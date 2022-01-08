import json
import logging
import pymysql.cursors

from pycoingecko import CoinGeckoAPI

log = logging.getLogger(__name__)


class PriceMsg:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price


class DbClient:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host,
                            user=user,
                            password=password,
                            database=db,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)
        self.symbols = set()

        with self.connection.cursor() as cursor:
            sql = f"SELECT `symbol` FROM `{table}`"
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                symbol = row['symbol']
                self.symbols.add(symbol)

    def write_data(self, table: str, price_data):
        self.connection.ping()
        with self.connection.cursor() as cursor:
            # Create a new record
            if price_data.symbol in self.symbols:
                sql = f"UPDATE {table} SET price='{price_data.price}' WHERE symbol='{price_data.symbol}'"
            else:
                sql = f"INSERT INTO {table} (symbol, price) VALUES ('{price_data.symbol}', '{price_data.price}')"
            log.info(f"Executing, {sql}")
            cursor.execute(sql)

        self.connection.commit()


if __name__ == '__main__':
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d,%H:%M:%S")

    db_client = DbClient("arufaresearch.mysql.pythonanywhere-services.com", "arufaresearch", "mysql@info", "arufaresearch$prices")

    # create coingecko API object
    cg = CoinGeckoAPI()

    coins_list = json.load(open('./coins.json'))['coins']
    for coin in coins_list:
        coin_price = cg.get_price(ids=coin['name'], vs_currencies='usd')[coin['name']]['usd']
        print(coin['symbol'], coin_price)
        price_data = PriceMsg(coin['symbol'], str(coin_price))
        db_client.write_data('prices', price_data)
