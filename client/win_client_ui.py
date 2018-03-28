# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win_client.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(510, 344)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.chat_view = QtWidgets.QListView(self.centralwidget)
        self.chat_view.setObjectName("chat_view")
        self.verticalLayout_2.addWidget(self.chat_view)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.update_button = QtWidgets.QPushButton(self.centralwidget)
        self.update_button.setText("")
        self.update_button.setObjectName("update_button")
        self.update_button.setIcon(QtGui.QIcon('logotip-3.png'))
        self.update_button.setIconSize(QtCore.QSize(30, 30))
        self.horizontalLayout_2.addWidget(self.update_button)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_to = QtWidgets.QLabel(self.centralwidget)
        self.label_to.setObjectName("label_to")
        self.horizontalLayout.addWidget(self.label_to)
        self.cbx_contacts = QtWidgets.QComboBox(self.centralwidget)
        self.cbx_contacts.setObjectName("cbx_contacts")
        self.horizontalLayout.addWidget(self.cbx_contacts)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.send_text = QtWidgets.QLineEdit(self.centralwidget)
        self.send_text.setObjectName("send_text")
        self.verticalLayout.addWidget(self.send_text)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.send_button = QtWidgets.QPushButton(self.centralwidget)
        self.send_button.setObjectName("send_button")
        self.horizontalLayout_2.addWidget(self.send_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Чат-клиент"))
        self.update_button.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic; color:#0000ff;\">Обновить контакты</span></p></body></html>"))
        self.label_to.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; font-style:italic; color:#ff0000;\">Кому</span></p></body></html>"))
        self.label_to.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600; font-style:italic; color:#ff0000;\">Кому</span></p></body></html>"))
        self.send_button.setText(_translate("MainWindow", "Отправить"))

