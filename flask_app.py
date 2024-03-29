import logging
import threading
import pymysql.cursors
from flask import Flask, jsonify

from utils.singleton import Singleton

app = Flask(__name__)
log = logging.getLogger(__name__)


class EventDbReader(metaclass=Singleton):
    def __init__(self):
        self.initiated = False

    def init(self, host, user, password, db):
        self.initiated = True
        self.connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def query_data(self, table, chain_id, pool_addr):
        table_data = list()
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = f"SELECT `block_no`, `txn_hash`, `amount`, `winner` FROM `{table}` WHERE `chain_id`='{chain_id}' AND `pool_addr`='{pool_addr}'"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                block_no = int(row['block_no'])
                txn_hash = row['txn_hash']
                amount = int(row['amount'])
                winner = row['winner']

                table_data.append({
                    "block_no": block_no,
                    "txn_hash": txn_hash,
                    "amount": amount,
                    "winner": winner,
                })
        return table_data


class PriceDbReader(metaclass=Singleton):
    def __init__(self):
        self.initiated = False

    def init(self, host, user, password, db):
        self.initiated = True
        self.connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

    def query_price(self, table, symbol):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            sql = f"SELECT `price` FROM `{table}` WHERE `symbol`='{symbol}'"
            cursor.execute(sql)
            result = cursor.fetchone()
            return {'price': float(result['price'])}


@app.route('/')
def home():
    return 'This is REST server to fetch historical events related to panther.money contracts'

@app.route('/history/<chain_id>/<pool_addr>')
def history(chain_id, pool_addr):
    if EventDbReader().initiated == False:
        EventDbReader().init("arufaresearch.mysql.pythonanywhere-services.com", "arufaresearch", "mysql@info", "arufaresearch$events")
    db_data = EventDbReader().query_data('winnings_prod', chain_id, pool_addr)
    response = jsonify(db_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/price/<symbol>')
def price(symbol):
    if PriceDbReader().initiated == False:
        PriceDbReader().init("arufaresearch.mysql.pythonanywhere-services.com", "arufaresearch", "mysql@info", "arufaresearch$prices")
    db_data = PriceDbReader().query_price('prices', symbol)
    response = jsonify(db_data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d,%H:%M:%S")

    app.run()
