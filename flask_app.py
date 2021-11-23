import logging
import threading
from flask import Flask, jsonify

from event_reader import EventReader

app = Flask(__name__)

@app.route('/')
def home():
    return 'This is REST server to fetch historical events related to panther.money contracts'

@app.route('/history/<chain_id>/<pool_addr>')
def history(chain_id, pool_addr):
    return jsonify([
        {
            "timestamp": "aaa",
            "amount": EventReader().counter,
            "winners": ["ajay", "vijay"],
        },
        {
            "timestamp": "bbb",
            "amount": EventReader().counter,
            "winners": ["abc", "xyz"],
        },
    ])

@app.route('/user/<chain_id>/<pool_addr>/<user_addr>')
def user_history(chain_id, pool_addr, user_addr):
    return jsonify([
        {
            "timestamp": "aaa",
            "amount": EventReader().counter,
        },
        {
            "timestamp": "bbb",
            "amount": EventReader().counter,
        },
    ])

event_fetch_thread = threading.Thread(target=EventReader().start)
event_fetch_thread.start()

if __name__ == '__main__':
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%Y-%m-%d,%H:%M:%S")

    app_thread = threading.Thread(target=app.run)
    app_thread.start()
