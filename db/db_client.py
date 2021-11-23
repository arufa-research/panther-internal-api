import time
import logging
import threading
from web3 import Web3
import pymysql.cursors

from abi import AbiFactory
from constants import POOLS_MAP
from provider import Web3ProviderFactory

log = logging.getLogger(__name__)


class EventMsg:
    def __init__(self, chain_id, pool_addr, draw_ts, winners):
        self.chain_id = chain_id
        self.pool_addr = pool_addr
        self.draw_ts = draw_ts
        self.winners = winners  # addresses separated by &


class DbClient:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def write_data(self, table: str, event_data):
        with self.connection:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = f"INSERT INTO `{table}` (chain_id, pool_addr, draw_ts, winners) VALUES ({event_data.chain_id}, '{event_data.pool_addr}', '{event_data.draw_ts}', '{event_data.winners}')"
                cursor.execute(sql)

            self.connection.commit()


if __name__ == '__main__':
    # db_client = DbClient("arufaresearch.mysql.pythonanywhere-services.com", "arufaresearch", "mysql@info", "arufaresearch$events")

    for network, data in POOLS_MAP.items():
        if network != "HarmonyTestnet":
            continue
        chain_id = network['chain_id']
        rpc_url  = network['rpc_url']
        pools    = network['pools']

        for pool in pools:
            # fetch events for last 10 blocks

            w3_provider = Web3ProviderFactory().get_provider(network)
            pool_addr = pool['pool_addr']
            pool_abi  = AbiFactory().get_contract_abi('PrizePool')
            pool_contract = w3_provider.eth.contract(address=pool_addr, abi=pool_abi)

            block_number: int = w3_provider.eth.getBlock('latest').number
            filter = contract.events.Awarded.createFilter(
                fromBlock=block_number-10,
                toBlock=block_number
            )

            event_msgs = []
            for event in filter.get_all_entries():
                print(event)
                # event_msg = EventMsg(

                # )
                # event_msgs.append(event_msg)

    # event_data = EventMsg(
    #     1123,
    #     "0x13343463546534",
    #     "12334",
    #     "0x937983794873948&0x79463794629847923&0x7236984723984"
    # )
    # db_client.write_data("winnings", event_data)
