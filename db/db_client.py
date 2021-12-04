import time
import logging
import threading
from web3 import Web3
import pymysql.cursors
from collections import defaultdict

from abi import AbiFactory
from constants import POOLS_MAP
from provider import Web3ProviderFactory

log = logging.getLogger(__name__)


class EventMsg:
    def __init__(self, chain_id, pool_addr, block_no, txn_hash, amount, winner):
        self.chain_id = chain_id
        self.pool_addr = pool_addr
        self.block_no = block_no
        self.txn_hash = txn_hash
        self.amount = amount
        self.winner = winner


class DbClient:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def query_data(self, table: str):
        table_data = defaultdict(lambda: defaultdict(lambda: set()))
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = f"SELECT `chain_id`, `pool_addr`, `txn_hash`, `winner` FROM `{table}`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                chain_id = row['chain_id']
                pool_addr = row['pool_addr']
                txn_hash = row['txn_hash']
                winner = row['winner']

                event_key = txn_hash + winner
                table_data[chain_id][pool_addr].add(event_key)
        return table_data

    def write_data(self, table: str, event_data):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            # Create a new record
            sql = f"INSERT INTO {table} (chain_id, pool_addr, block_no, txn_hash, amount, winner) VALUES ('{event_data.chain_id}', '{event_data.pool_addr}', '{event_data.block_no}', '{event_data.txn_hash}', '{event_data.amount}', '{event_data.winner}')"
            log.info(f"Inserting into table, {sql}")
            cursor.execute(sql)

        self.connection.commit()


if __name__ == '__main__':
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d,%H:%M:%S")
    db_client = DbClient("arufaresearch.mysql.pythonanywhere-services.com", "arufaresearch", "mysql@info", "arufaresearch$events")

    # fetch and populate str(txn hash + winner addr) for each (chain_id, pool_addr)
    log.info(f"Fetching stored txns from db")
    db_hashes = db_client.query_data("winnings_prod")

    prev_block_number = dict()
    for network, data in POOLS_MAP.items():
        w3_provider = Web3ProviderFactory().get_provider(network)
        block_number = w3_provider.eth.getBlock('latest').number - 10000
        prev_block_number[network] = block_number

    while True:
        for network, data in POOLS_MAP.items():
            log.info(f"Fetching pool events for network: {network}")
            chain_id = int(data['chain_id'])

            w3_provider = Web3ProviderFactory().get_provider(network)
            latest_block_number = w3_provider.eth.getBlock('latest').number

            for pool in data['pools']:
                log.info(f"Fetching events for {pool['token_name']} pool")
                # fetch events from last fetched till latest block

                pool_addr = pool['pool_addr']
                pool_abi  = AbiFactory().get_contract_abi('PrizePool')
                pool_contract = w3_provider.eth.contract(address=pool_addr, abi=pool_abi)

                filter = pool_contract.events.Awarded.createFilter(
                    fromBlock=prev_block_number[network],
                    toBlock=latest_block_number
                )

                for event in filter.get_all_entries():
                    log.info(f"Event found on block: {event.blockNumber} with txn hash: {event.transactionHash.hex()}")
                    event_key = str(event.transactionHash.hex()) + str(event.args.winner)
                    if event_key in db_hashes[chain_id][pool_addr]:
                        log.info(f"Event with txn hash: {event.transactionHash.hex()} and winner {event.args.winner} exists in db, skipping")
                        continue
                    event_msg = EventMsg(
                        chain_id,
                        pool_addr,
                        event.blockNumber,
                        event.transactionHash.hex(),
                        event.args.amount,
                        event.args.winner
                    )
                    log.info(f"Inserting event with txn hash: {event.transactionHash.hex()} and winner {event.args.winner}, amount {event.args.amount} into db")
                    db_client.write_data("winnings_prod", event_msg)
                    db_hashes[chain_id][pool_addr].add(event_key)
            prev_block_number[network] = latest_block_number
        log.info(f"Sleeping for 2 mins")
        time.sleep(120) # 2 mins
