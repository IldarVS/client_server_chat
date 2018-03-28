import logging
from datetime import datetime
import select
import json
from crud import Crud
from storage_server import CClients, CHistory, CContacts
import auth
from log_run import log

logger = logging.getLogger('chat.controller')
code = "utf-8"
unix_time = datetime.now()

class ChatController:
    def __init__(self, server):
        self.__server = server
        self.__clients = server.clients
        self.__clients_name = server.clients_name

    @log
    @auth.Auth.login_required
    def send_message(self, user, messages, w_clients, name_clients):
        """
        Отсылает сообщение клиентам
        """
        for sock in w_clients:
            if sock in messages:
                try:
                    # Подготовить и отправить ответ сервера
                    resp = messages[sock]

                    if resp['action'] == 'run_contact':
                        usr = Crud(CClients)
                        user_list = []
                        crud_objects = usr.read_crud()
                        for crud_object in crud_objects:
                            user_list.append(str(crud_object))
                        user_list = tuple(user_list)
                        message = {'action': 'run_contact', 'auth': user_list}
                        message = json.dumps(message).encode(code)
                        sock.send(message)
                    elif resp['action']== 'msg':
                        message = resp
                        contacts = Crud(CContacts)
                        contacts.add_crud(int(message['from']), int(message['to']))
                        users = Crud(CClients)
                        user_from = users.read_crud_id(int(message['from']))
                        if int(message['to']) == 0:
                            user_to = [0,"All"]
                        else:
                            user_to = users.read_crud_id(int(message['to']))
                        message = json.dumps(message).encode(code)
                        for sock in w_clients:
                            for name_client in name_clients:
                                if user_to[1] == "All":
                                    if name_client[0]!= user_from[1]:
                                        sock.send(message)
                                elif name_client[0] == user_to[1] and name_client[1] == sock.getpeername():
                                    sock.send(message)

                except:  # Сокет недоступен, клиент  отключился
                    print('Клиент {} отключился'.format(sock.getpeername()))
                    sock.close()
                    w_clients.remove(sock)
                    name_clients.remove(name_client)


    @log
    def get_message(self, user, r_clients, all_clients):
        """
        Получает сообщение от клиентов
        """

        responses = {}  # Словарь ответов сервера вида {сокет:  запрос}

        for sock in r_clients:
            try:
                data = json.loads(sock.recv(2048).decode(code))
                responses[sock] = data
            except:
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                all_clients.remove(sock)
        return responses

    @log
    def message_cycle(self,name): # ,
        while True:
            self.user = ''
            try:
                conn, addr = self.__server.socket.accept()
            except OSError as e:
                pass
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                kwargs = json.loads(conn.recv(2048).decode(code))
                if kwargs['action'] == 'authenticate':
                    usr = auth.Auth(**kwargs)
                    msg, login = usr.authent()
                    conn.send(login)
                elif kwargs['action'] == 'registration':
                    usr = auth.Auth(**kwargs)
                    msg, login = usr.new_reg()  # new registration account
                    conn.send(login)
                else:
                    conn.close()



                if msg != 'exit' and msg != 'run_contact':
                    self.user = msg
                    if (msg, addr) not in self.__clients_name:
                        self.__clients_name.append((msg, addr))
                        self.__clients.append(conn)
                        for conn1 in self.__clients:
                            if conn1 != conn:
                                try:
                                   conn1.send(login)
                                except Exception:
                                    pass
                                    # self.__clients.remove(conn1)
                                # else:
                                    # continue


                    usr = auth.Auth(**kwargs)
                    usr.registrat()
            finally:
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.__clients, self.__clients,
                                            [], wait)

                except Exception:
                    pass

                requests = self.get_message(self.user, r, self.__clients)
                self.send_message(self.user, requests, w, self.__clients_name)
    print('Чат запущен!')