# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ChatRoom.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
    # Add other methods for signup, room creation, etc.
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1528, 1103)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.ChatTable = QtWidgets.QFrame(self.centralwidget)
        self.ChatTable.setStyleSheet("QFrame{\n"
"    background:rgb(41, 41, 41)\n"
"}")
        self.ChatTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ChatTable.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ChatTable.setObjectName("ChatTable")
        self.pushButton_6 = QtWidgets.QPushButton(self.ChatTable)
        self.pushButton_6.setGeometry(QtCore.QRect(1230, 910, 221, 61))
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"    background: rgb(100, 200, 100);\n"
"    border: none;\n"
"    border-radius: 25px;\n"
"    }\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 rgb(100, 200, 100), \n"
"                                stop:1 rgb(120, 220, 120)  \n"
"                               );\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.textEdit = QtWidgets.QTextEdit(self.ChatTable)
        self.textEdit.setGeometry(QtCore.QRect(510, 910, 711, 61))
        self.textEdit.setStyleSheet("QTextEdit{\n"
"    background: rgb(203, 203, 203);\n"
"    border-radius: 12px;\n"
"\n"
"}")
        self.textEdit.setObjectName("textEdit")
        self.listWidget = QtWidgets.QListWidget(self.ChatTable)
        self.listWidget.setGeometry(QtCore.QRect(510, 10, 951, 881))
        self.listWidget.setStyleSheet("QListWidget {\n"
"    background-color: #e0e0e0; \n"
"}\n"
"\n"
"QListWidget::item {\n"
"    background-color: #ffffff;\n"
"    border-radius: 10px;\n"
"    padding: 10px; /* 设置内边距 */\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #c0c0c0;\n"
"}\n"
"")
        self.listWidget.setObjectName("listWidget")
        self.layoutWidget = QtWidgets.QWidget(self.ChatTable)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 491, 281))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_2 = QtWidgets.QTextEdit(self.ChatTable)
        self.textEdit_2.setGeometry(QtCore.QRect(20, 720, 451, 61))
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
"    background: rgb(203, 203, 203);\n"
"    border-radius: 12px;\n"
"\n"
"}")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_2 = QtWidgets.QLabel(self.ChatTable)
        self.label_2.setGeometry(QtCore.QRect(20, 540, 451, 161))
        self.label_2.setStyleSheet("QLabel{\n"
"    background:rgb(145, 145, 145);\n"
"    border-radius: 20px;\n"
"}")
        self.label_2.setObjectName("label_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.ChatTable)
        self.textEdit_3.setGeometry(QtCore.QRect(20, 810, 451, 61))
        self.textEdit_3.setStyleSheet("QTextEdit{\n"
"    background: rgb(203, 203, 203);\n"
"    border-radius: 12px;\n"
"\n"
"}")
        self.textEdit_3.setObjectName("textEdit_3")
        self.pushButton_7 = QtWidgets.QPushButton(self.ChatTable)
        self.pushButton_7.setGeometry(QtCore.QRect(10, 910, 221, 61))
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"    background: rgb(100, 200, 100);\n"
"    border: none;\n"
"    border-radius: 25px;\n"
"    }\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 rgb(100, 200, 100), \n"
"                                stop:1 rgb(120, 220, 120)  \n"
"                               );\n"
"}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.ChatTable)
        self.pushButton_8.setGeometry(QtCore.QRect(250, 910, 221, 61))
        self.pushButton_8.setStyleSheet("QPushButton{\n"
"    background: rgb(100, 200, 100);\n"
"    border: none;\n"
"    border-radius: 25px;\n"
"    }\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                stop:0 rgb(100, 200, 100), \n"
"                                stop:1 rgb(120, 220, 120)  \n"
"                               );\n"
"}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.listWidget_2 = QtWidgets.QListWidget(self.ChatTable)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 10, 489, 521))
        self.listWidget_2.setStyleSheet("QListWidget{\n"
"background:rgb(188, 188, 188);\n"
"}")
        self.listWidget_2.setObjectName("listWidget_2")
        self.gridLayout.addWidget(self.ChatTable, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1528, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_6.setText(_translate("MainWindow", "Send"))
        self.textEdit_2.setPlaceholderText(_translate("MainWindow", "Username"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.textEdit_3.setPlaceholderText(_translate("MainWindow", "Passowrd"))
        self.pushButton_7.setText(_translate("MainWindow", "LogIn"))
        self.pushButton_8.setText(_translate("MainWindow", "SignUP"))
class BubbleDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if not index.isValid():
            return

        # Set up the painter
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)

        # Set up colors and styles based on user role
        user_role = index.data(QtCore.Qt.UserRole)
        if user_role == "outgoing":
            bubble_color = QtGui.QColor(100, 200, 100)
            text_color = QtGui.QColor(255, 255, 255)
            align = QtCore.Qt.AlignRight
        else:
            bubble_color = QtGui.QColor(41, 41, 41)
            text_color = QtGui.QColor(255, 255, 255)
            align = QtCore.Qt.AlignLeft

        # Draw the bubble
        bubble_rect = option.rect.adjusted(5, 5, -5, -5)
        painter.setBrush(bubble_color)
        painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))
        painter.drawRoundedRect(bubble_rect, 10, 10)

        # Draw the text
        text_rect = bubble_rect.adjusted(10, 10, -10, -10)
        painter.setPen(QtGui.QPen(text_color, 2))
        painter.drawText(text_rect, align | QtCore.Qt.AlignTop, index.data())

    def sizeHint(self, option, index):
        return QtCore.QSize(300, 50)

