

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1497, 1081)
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
        self.textEdit.setObjectName("textEdit")
        self.listWidget = QtWidgets.QListWidget(self.ChatTable)
        self.listWidget.setGeometry(QtCore.QRect(510, 10, 961, 881))
        self.listWidget.setStyleSheet("QListWidget {\n"
                                      "    background-color: #e0e0e0; \n"
                                      "}")
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.listWidget.setItemDelegate(BubbleDelegate())
        self.widget = QtWidgets.QWidget(self.ChatTable)
        self.widget.setGeometry(QtCore.QRect(10, 10, 491, 281))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.gridLayout.addWidget(self.ChatTable, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1497, 30))
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
        self.pushButton.setText(_translate("MainWindow", "Chatroom1"))
        self.pushButton_2.setText(_translate("MainWindow", "Chatroom2"))
        self.pushButton_4.setText(_translate("MainWindow", "Chatroom3"))
        self.pushButton_3.setText(_translate("MainWindow", "Chatroom4"))
        self.pushButton_5.setText(_translate("MainWindow", "Chatroom5"))


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
