'''класс Сервер'''
from socket import socket, AF_INET, SOCK_STREAM
import argparse
from datetime import datetime
from log_run import log
import chat_controller
from threading import Thread, Lock, RLock

code = "utf-8"
unix_time = datetime.now()

class Server:
    def __init__(self):
        self.__sock = socket(AF_INET, SOCK_STREAM)
        self.__sock.bind(address)
        self.__sock.listen(20)
        self.__sock.settimeout(0.2)
        self.__clients = []
        self.__clients_name = []

    @property
    def clients(self):
        return self.__clients

    @property
    def clients_name(self):
        return self.__clients_name

    @property
    def socket(self):
        return self.__sock


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", type=str, default="127.0.0.1", help="our_ip")
    parser.add_argument("-p", type=int, default=7777, help="our_port")
    args = parser.parse_args()
    address = (args.a, args.p)
    server = Server()
    controller = chat_controller.ChatController(server)
    # controller.message_cycle()
    TClientThr = Thread(target = controller.message_cycle, args=("ThreadClient",))
    TClientThr.start()

