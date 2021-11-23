import time
import logging
import threading

# from utils.constants import CHAIN_IDS
from utils.singleton import Singleton

log = logging.getLogger(__name__)


class EventReader(metaclass=Singleton):
    def __init__(self):
        log.info("EventReader initiated")
        self.counter = 0
        self.started = False

    def start(self):
        log.info("EventReader thread started")
        self.started = True
        while True:
            self.counter += 1
            time.sleep(2) # 2 mins
