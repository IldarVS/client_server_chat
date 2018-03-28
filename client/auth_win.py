import sys
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
# from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
# from PyQt5.QtGui import QIcon

from auth_user_ui import Ui_MainWindow as ui_class

class CMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.ui = ui_class()
        self.ui.setupUi(self)
    #     self.model = QtGui.QStandardItemModel()
    #     self.ui.chat_view.setModel(self.model)
        self.ui.ok_button.pressed.connect(self.auth)
        self.ui.ok_button.pressed.connect(self.close)
        self.ui.cansel_button.pressed.connect(self.close)
    #
    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.ui.ok_button.pressed.emit()
        elif e.key() == 16777216:
            self.ui.cansel_button.pressed.emit()
        #


    def auth(self):
        username = self.ui.name_line.text()
        password = self.ui.pass_line.text()
        print(username, password)
        # self.ui.cansel_button.pressed.emit()
        return username, password




    # def send_mess(self):
    #
    #     msg = self.ui.send_text.text()
    #     self.ui.send_text.setText("")
    #     #отправить
    #     # получить
    #     answer = "Ответ на сообщение"
    #     item = QtGui.QStandardItem()
    #     item.setData("[Мы сказали]>> %s" % msg, QtCore.Qt.DisplayRole)
    #     self.model.invisibleRootItem().appendRow(item)
    #
    #     answ_item = QtGui.QStandardItem()
    #     answ_item.setData("[Собеседник сказал]>> %s" % answer, QtCore.Qt.DisplayRole)
    #     self.model.invisibleRootItem().appendRow(answ_item)