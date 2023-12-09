from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import socketio


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1548, 1103)
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
        self.listWidget.setGeometry(QtCore.QRect(510, 40, 951, 851))
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
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_5 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        self.label = QtWidgets.QLabel(self.ChatTable)
        self.label.setGeometry(QtCore.QRect(510, 10, 951, 31))
        self.label.setStyleSheet("QLabel{\n"
                                 "    background:rgb(255, 255, 255);\n"
                                 "}")
        self.label.setObjectName("label")
        self.textEdit_2 = QtWidgets.QTextEdit(self.ChatTable)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 910, 451, 61))
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
                                      "    background: rgb(203, 203, 203);\n"
                                      "    border-radius: 12px;\n"
                                      "\n"
                                      "}")
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.ChatTable, 0, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1548, 30))
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
        self.label.setText(_translate("MainWindow", "chatroomX"))


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
            bubble_color = QtGui.QColor(100, 200, 100)  # 微信聊天中的出going气泡颜色
            text_color = QtGui.QColor(255, 255, 255)
            align = QtCore.Qt.AlignRight
        else:
            bubble_color = QtGui.QColor(223, 223, 223)  # 微信聊天中的incoming气泡颜色
            text_color = QtGui.QColor(0, 0, 0)
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


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    send_message_signal = QtCore.pyqtSignal(name='sendMessage')  # 添加 name 参数

    def __init__(self):
        super(MyMainWindow, self).__init__()

        self.setupUi(self)
        # Connect the Send button to the send_message function
        self.pushButton_6.clicked.connect(self.send_message_signal)

        # Connect other buttons to switch_chat_room function
        self.pushButton.clicked.connect(lambda: self.switch_chat_room("ChatRoom1"))
        self.pushButton_2.clicked.connect(lambda: self.switch_chat_room("ChatRoom2"))
        self.pushButton_3.clicked.connect(lambda: self.switch_chat_room("ChatRoom3"))
        self.pushButton_4.clicked.connect(lambda: self.switch_chat_room("ChatRoom4"))
        self.pushButton_5.clicked.connect(lambda: self.switch_chat_room("ChatRoom5"))

        # Initialize current chat room and messages dictionary
        self.current_chat_room = "ChatRoom1"
        self.chat_room_messages = {"ChatRoom1": [], "ChatRoom2": [], "ChatRoom3": [], "ChatRoom4": [], "ChatRoom5": []}

        # Set up delegate for listWidget
        self.listWidget.setItemDelegate(BubbleDelegate())

        # 创建 SocketIO 连接
        self.sio = socketio.Client()
        # Connect to server events
        self.sio.on('message_from_server', self.handle_server_response)

        self.sio_thread = threading.Thread(target=self.init_socketio)
        self.sio_thread.start()

    def init_socketio(self):
        # Connect to the SocketIO server
        self.sio = socketio.Client()
        self.sio.connect('http://127.0.0.1:5000', namespaces=['/'])
        self.sio.on('connect', self.handle_connect)
        self.sio.on('disconnect', self.handle_disconnect)
        self.sio.on('online_users', self.handle_online_users)
        self.sio.on('receive_message', self.handle_receive_message)
        self.sio.wait()

    def handle_connect(self):
        print('Connected to server')

    def handle_disconnect(self):
        print('Disconnected from server')

    def handle_online_users(self, online_users):
        print('Online Users:', online_users)
        # You can update the UI with the online_users data if needed

    def handle_receive_message(self, data):
        print('Received message:', data)

        # You can update the UI with the received message data if needed

    def switch_chat_room(self, new_chat_room):
        if new_chat_room != self.current_chat_room:
            # Save messages for the current chat room
            self.chat_room_messages[self.current_chat_room] = self.get_messages()

            # Update current chat room
            self.current_chat_room = new_chat_room

            # Update listWidget with messages for the new chat room
            self.update_list_widget()

            # Update label to display current chat room
            self.label.setText(f"{new_chat_room}")

    def add_message(self, text, user_role):
        item = QtWidgets.QListWidgetItem(text)
        item.setData(QtCore.Qt.UserRole, user_role)
        self.listWidget.addItem(item)

    def send_message(self):
        message_text = self.textEdit.toPlainText()
        if message_text:
            # 发送消息到服务器
            user_name = self.textEdit_2.toPlainText()
            self.sio.emit('message_from_ui', {'text': message_text, 'user': user_name})

    def update_list_widget(self):
        # Clear the listWidget
        self.listWidget.clear()

        # Populate the listWidget with messages for the current chat room
        messages = self.chat_room_messages.get(self.current_chat_room, [])
        for message in messages:
            self.add_message(message["text"], message["user_role"])

    def get_messages(self):
        # Retrieve messages from the listWidget for the current chat room
        messages = []
        for row in range(self.listWidget.count()):
            item = self.listWidget.item(row)
            text = item.text()
            user_role = item.data(QtCore.Qt.UserRole)
            messages.append({"text": text, "user_role": user_role})
        return messages

    def handle_server_response(self, data):
        print('Received response from server:', data)
        # 在这里更新 UI
        text = data.get('text', '')
        user_role = data.get('user_role', '')
        self.add_message(text, user_role)


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication([])
        window = MyMainWindow()
        window.show()
        app.exec_()
    except Exception as e:
        print(f"An error occurred: {e}")
