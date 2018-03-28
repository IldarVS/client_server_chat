# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'auth_user.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(299, 116)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setInputMethodHints(QtCore.Qt.ImhNone)
        self.name_label.setObjectName("name_label")
        self.verticalLayout.addWidget(self.name_label)
        self.pass_label = QtWidgets.QLabel(self.centralwidget)
        self.pass_label.setObjectName("pass_label")
        self.verticalLayout.addWidget(self.pass_label)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.name_line = QtWidgets.QLineEdit(self.centralwidget)
        self.name_line.setObjectName("name_line")
        self.verticalLayout_2.addWidget(self.name_line)
        self.pass_line = QtWidgets.QLineEdit(self.centralwidget)
        self.pass_line.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pass_line.setObjectName("pass_line")
        self.verticalLayout_2.addWidget(self.pass_line)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.ok_button = QtWidgets.QPushButton(self.centralwidget)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_3.addWidget(self.ok_button)
        self.cansel_button = QtWidgets.QPushButton(self.centralwidget)
        self.cansel_button.setObjectName("cansel_button")
        self.horizontalLayout_3.addWidget(self.cansel_button)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Подключение к чату"))
        self.name_label.setText(_translate("MainWindow", "Имя пользователя"))
        self.pass_label.setText(_translate("MainWindow", "Пароль"))
        self.ok_button.setText(_translate("MainWindow", "OK"))
        self.cansel_button.setText(_translate("MainWindow", "Отмена"))

