from socket import *
from select import select
import sys
import json
from datetime import datetime
import argparse
from log_run import log

unix_time = datetime.now()

class ChatClient:
    def __init__(self, sock, message):
        self.__message = message
        self.sock = sock
        self.coding = "utf-8"
        self.__answers='exit'

    def send(self):
        self.sock.send(self.__message)

    @log
    def answer(self):
        self.__answers = json.loads(self.sock.recv(2048).decode(self.coding))

        return self.__answers

    @property
    def message(self):
        return self.__message

    @log
    def encode(self):
        self.__message = json.dumps(self.__message).encode(self.coding)

