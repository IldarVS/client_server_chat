import sys,os
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from socket import *
import json
from datetime import datetime
import time
import chat
from crud_user import Crud
from storage_client import CContactUser, CHistoryMessage
from threading import Thread, Lock, RLock
import generate


code = "utf-8"


from win_client_ui import Ui_MainWindow as ui_class
from auth_user_ui import Ui_MainWindow as ui_class_2

class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, answer, username, sock, parent=None):
        super().__init__(parent)
        self.answer = answer
        self.username = username
        self.update_cont =""
        self.__sock = sock
        self.ui = ui_class()
        self.ui.setupUi(self)
        self.lock_send = Lock()
        self.lock_answer = Lock()
        self.model = QtGui.QStandardItemModel()
        self.ui.chat_view.setModel(self.model)
        self.ui.send_button.pressed.connect(self.select_send_mess)
        self.ui.update_button.pressed.connect(self.update_contact_end)
        self.answer_auth()
        self.box_contacts()


    def closeEvent(self,event):
        reply = QtWidgets.QMessageBox.question(self,
           'Выход', "Выйти из программы?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
           QtWidgets.QMessageBox.No)
        if reply ==QtWidgets.QMessageBox.Yes:
            self.send_mess("Всем", "вышел из чата")
            event.accept()
        else:
            event.ignore()

    def answer_auth(self):
        item = QtGui.QStandardItem()
        item.setData("Направлен запрос на соединение...", QtCore.Qt.DisplayRole)
        self.model.invisibleRootItem().appendRow(item)
        answ_item = QtGui.QStandardItem()
        answ_item.setData("%s" % self.answer, QtCore.Qt.DisplayRole)
        self.model.invisibleRootItem().appendRow(answ_item)
        self.answerThr = Thread(target=self.answers_mess, args=("ThreadAnswer",self.__sock))
        self.answerThr.daemon = True
        self.answerThr.start()
        self.update_contact()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.ui.send_button.pressed.emit()

    def box_contacts(self):
        users = Crud(CContactUser)
        self.list_users = users.read_crud()
        for _ in self.list_users:
            a =_.split(',')
            if self.username != a[1]:
                self.ui.cbx_contacts.addItem(a[1])

    def update_contact(self):
        self.__message = {
            "action": "run_contact",
            "time": str(datetime.now())
        }
        data = chat.ChatClient(self.__sock, self.__message)
        data.encode()
        data.send()

    def update_contact_end(self):
        users = Crud(CContactUser)
        count_upd_contacts = 0
        for _ in self.update_cont:
            new_contact = _.split(',')
            args = (int(new_contact[0]), new_contact[1], new_contact[2])
            users.add_crud(*args)
        self.list_users = users.read_crud()
        for _ in self.list_users:
            upd_contact = _.split(',')
            gid = int(upd_contact[0])
            for _ in self.update_cont:
                new_contact = _.split(',')
                kwargs = {'usergid': int(new_contact[0]), 'username': new_contact[1],
                          'information': new_contact[2]}
                if int(new_contact[0]) == gid:
                    count_upd_contacts += 1
                    users.upd_crud(gid, **kwargs)
        args = (0, "Всем", "Всем")
        users.add_crud(*args)
        self.ui.cbx_contacts.clear()
        self.box_contacts()
        upd_item = QtGui.QStandardItem()
        upd_item.setData("Обновленных контактов = %s" % count_upd_contacts, QtCore.Qt.DisplayRole)
        self.model.invisibleRootItem().appendRow(upd_item)

    def select_username(self, user_id):
        for _ in self.list_users:
            a = _.split(',')
            if a[0] == user_id:
                return a[1]

    def select_user_id(self, contacts):
        for _ in self.list_users:
            a = _.split(',')
            if a[1] == contacts:
                return a[0]

    def select_send_mess(self):
        self.send_mess(self.ui.cbx_contacts.currentText())

    def send_mess(self, contacts, msgs = None):
        self.id_select_user = self.select_user_id(contacts)
        self.user_id = self.select_user_id(self.username)
        mess = Crud(CHistoryMessage)
        if msgs is None:
            message = self.ui.send_text.text()
        else:
            message = msgs
        item = QtGui.QStandardItem()
        item.setData("{} to {} >> {}".format(self.username, contacts, message), QtCore.Qt.DisplayRole)
        self.model.invisibleRootItem().appendRow(item)
        mesk = generate.MessKeys(message)
        message = mesk.send_keys()
        self.ui.send_text.setText("")
        self.__message = {"action": "msg",
                          "time": str(datetime.now()),
                          "to": self.id_select_user,
                          "from": self.user_id,
                          "message": message
                          }
        args = (int(self.user_id), int(self.id_select_user), message, str(datetime.now()))
        self.lock_send.acquire()
        mess.add_crud(*args)
        self.lock_send.release()
        self.sendThr = Thread(target=self.sending_mess, args=("ThreadSend", self.__sock, self.__message))
        self.sendThr.start()

    def sending_mess(self, name, sock, message):
        data = chat.ChatClient(sock, message)
        self.lock_send.acquire()
        data.encode()
        data.send()
        self.lock_send.release()

    def answers_mess(self, name, sock):
        mess = Crud(CHistoryMessage)
        try:
            while True:
                data = chat.ChatClient(sock, "")
                self.__answers = data.answer()
                answ_item = QtGui.QStandardItem()
                if self.__answers["action"] == "connect":
                    print(self.__answers["action"])
                    self.__answers = self.__answers
                    answ_item.setData(self.__answers["auth"], QtCore.Qt.DisplayRole)
                    self.model.invisibleRootItem().appendRow(answ_item)
                elif self.__answers["action"] == "run_contact":
                    print(self.__answers["action"])
                    self.__answers = self.__answers
                    self.update_cont = self.__answers["auth"]
                elif self.__answers["action"] == "msg":
                    user_from = self.select_username(self.__answers["from"])
                    user_to = self.username
                    mesk = generate.MessKeys(self.__answers["message"])
                    message = mesk.answer_keys()
                    self.lock_answer.acquire()
                    args = (int(self.__answers["from"]), int(self.__answers["to"]), message, self.__answers["time"])
                    mess.add_crud(*args)
                    self.lock_answer.release()
                    answ_item.setData("{}>> сообщение от {}: {}".format(user_to, user_from, message), QtCore.Qt.DisplayRole)
                    self.model.invisibleRootItem().appendRow(answ_item)
                time.sleep(0.2)
        except:
            pass

class CAuth(QtWidgets.QMainWindow):
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

        self.con_server()

    def con_server(self):
        self.address = ('127.0.0.1',7777)
        # self.port = 7777
        # address = (self.address, self.port)

        account = {
            "action": "authenticate",
            "time": str(datetime.now()),
            "user": {
                "account_name": self.username,
                "password": self.password
            }
        }
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.client = Client(self.sock, self.address, self.username)
        reg = self.client.action(**account)
        if reg == 'y':
            inform, ok = QtWidgets.QInputDialog.getText(self, 'Информация'
                    , 'Введите информацию  о пользователе %s: ' % self.username)

            if ok:
                pass
            else:
                inform = self.username

            account = {
                "action": "registration",
                "time": str(datetime.now()),
                "user": {
                    "account_name": self.username,
                    "password": self.password,
                    "information": inform
                }
            }
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.client = Client(self.sock, self.address, self.username)
            reg = self.client.action(**account)




class CAuthWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        # self.isVisible = True
        self.username =''
        self.password =''
        self.ui = ui_class_2()
        self.ui.setupUi(self)
        self.ui.ok_button.pressed.connect(self.auth)
        self.ui.ok_button.pressed.connect(self.close)
        self.ui.cansel_button.pressed.connect(QtWidgets.QApplication.quit)
    #
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return:
            self.ui.ok_button.pressed.emit()
        elif e.key() == QtCore.Qt.Key_Escape:
            self.ui.cansel_button.pressed.emit()
        #

    def auth(self):
        h = generate.get_hash(self.ui.name_line.text(), self.ui.pass_line.text())
        self.open_auth = CAuth(self.ui.name_line.text(), h)  # передаём в конструктор значения lineEdit_user и lineEdit_passwd


class Client(QtWidgets.QMainWindow):
    def __init__(self, sock, address,username):
        super().__init__()
        self.username = username
        self.__sock = sock
        self.__conn = "connection"
        try:
            self.__sock.connect(address)
        except ConnectionRefusedError:
            self.__conn = None
            QtWidgets.QMessageBox.information(self, "Соединение...",
                            "сервер не найден, Приложентн будет закрыто", QtWidgets.QMessageBox.Ok)
    def action(self, **kwargs):
        if self.__conn != None:
            self.__message = kwargs
            self.__answers = ''
            data = chat.ChatClient(self.__sock, self.__message)
            data.encode()
            data.send()
            self.__answers = data.answer()
            answer = self.__answers['auth']
            reg = 'n'

            if self.__answers['msg'] == 'exit':
                self.__sock.close
                self.wnd = CAuthWindow()
                self.wnd.show()
                answer = answer +'\n'
                with open("answer.txt",'+a') as f:
                    f.writelines(answer)
            elif self.__answers['msg'] == 'noreg':
                self.__sock.close
                self.__answers['msg'] = 'exit'
                answer = answer + '\n'
                with open("answer.txt", '+a') as f:
                    f.writelines(answer)

                reply = QtWidgets.QMessageBox.question(self, 'Регистрация', 'Будете регистрироваться(Yes/No)?',
                                                       QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                       QtWidgets.QMessageBox.Yes)
                if reply == QtWidgets.QMessageBox.Yes:
                    reg ='y'
                else:
                    self.wnd = CAuthWindow()
                    self.wnd.show()

                return reg
            else:
                answer = answer + '\n'
                with open("answer.txt", '+a') as f:
                    f.writelines(answer)
                with open("answer.txt", 'r') as f:
                    answer = f.read()
                os.remove("answer.txt")

                self.open_main = CMainWindow(answer, self.username, self.__sock)
                self.open_main.show()


