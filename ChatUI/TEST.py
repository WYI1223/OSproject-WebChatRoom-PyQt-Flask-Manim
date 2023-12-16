from PyQt5 import QtCore, QtGui, QtWidgets
import ChatRoom_ui
import sys
from PyQt5.QtWidgets import QListWidgetItem, QPushButton

# 导入 SocketIO
from socketIO_client import SocketIO


class ChatClient(QtCore.QObject):
    messageReceived = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 建立 SocketIO 连接
        self.socket = SocketIO('http://127.0.0.1:5000')
        self.connect_signals()

    def connect_signals(self):
        self.socket.on('connect', self.handle_connect)
        self.socket.on('receive_message', self.handle_receive_message)

    def handle_connect(self, *args):
        if self.socket.connected:
            print("Connected to server")
        else:
            print("Failed to connect")

        # 连接成功后的处理

    def handle_receive_message(self, data):
        self.messageReceived.emit(data)

    def login(self, username, password):
        self.socket.emit('login', {'username': username, 'password': password})

    # 添加其他方法用于注册、创建聊天室等操作


class MyMainWindow(QtWidgets.QMainWindow, ChatRoom_ui.Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        # 创建 ChatClient 实例
        self.chat_client = ChatClient()
        self.chat_client.messageReceived.connect(self.handle_message_received)

        self.setupUi(self)

        # 连接按钮的点击事件
        self.pushButton_6.clicked.connect(self.handle_send_message)
        self.pushButton_7.clicked.connect(self.handle_login)
        self.pushButton_8.clicked.connect(self.handle_signup)

        # 初始化列表和按钮
        self.listWidget_1.setItemDelegate(ChatRoom_ui.BubbleDelegate())
        self.listWidget_2.itemClicked.connect(self.handle_chatroom_clicked)

        # 显示默认的聊天室信息
        self.update_chatroom_list(['Room1', 'Room2'])

    def handle_send_message(self):
        # 实现发送消息的逻辑
        username = self.textEdit_2.toPlainText()
        message = self.textEdit.toPlainText()
        room_id = 123  # 用实际的聊天室 ID 替换
        self.chat_client.socket.emit('send_message', {'username': username, 'room': room_id, 'message': message})

    def handle_login(self):
        # 实现登录逻辑
        username = self.textEdit_2.toPlainText()
        password = self.textEdit_3.toPlainText()
        self.chat_client.login(username, password)

    def handle_signup(self):
        # 实现注册逻辑
        pass

    def handle_chatroom_clicked(self, item):
        # 切换聊天室时的处理逻辑
        new_chat_room = item.text()
        self.switch_chat_room(new_chat_room)

    def switch_chat_room(self, new_chat_room):
        # 处理切换聊天室的逻辑
        if new_chat_room != self.current_chat_room:
            # 保存当前聊天室的消息
            self.chat_room_messages[self.current_chat_room] = self.get_messages()

            # 更新当前聊天室
            self.current_chat_room = new_chat_room

            # 更新列表显示
            self.update_list_widget()

            # 更新标签显示当前聊天室
            self.label_2.setText(f"Current Chat Room: {new_chat_room}")

    def handle_message_received(self, data):
        # 处理接收到的消息
        text = f"{data['username']} ({data['created_at']}): {data['message']}"
        self.add_message(text, "incoming")

    def add_message(self, text, user_role):
        # 添加消息到列表
        item = QtWidgets.QListWidgetItem(text)
        item.setData(QtCore.Qt.UserRole, user_role)
        self.listWidget_1.addItem(item)

    def update_list_widget(self):
        # 清空列表
        self.listWidget_1.clear()

        # 获取当前聊天室的消息
        messages = self.chat_room_messages.get(self.current_chat_room, [])

        # 将消息添加到列表
        for message in messages:
            self.add_message(message["text"], message["user_role"])

    def get_messages(self):
        # 从列表获取当前聊天室的消息
        messages = []
        for row in range(self.listWidget_1.count()):
            item = self.listWidget_1.item(row)
            text = item.text()
            user_role = item.data(QtCore.Qt.UserRole)
            messages.append({"text": text, "user_role": user_role})
        return messages

    def update_chatroom_list(self, chatrooms):
        # 更新聊天室列表
        self.listWidget_2.clear()
        for chatroom in chatrooms:
            button = QPushButton(chatroom)
            item = QtWidgets.QListWidgetItem()
            self.listWidget_2.addItem(item)
            self.listWidget_2.setItemWidget(item, button)

    def update_login_info(self, username, status):
        # 更新登录信息
        self.label_3.setText(f"Logged in as: {username}")
        self.label_4.setText(f"Status: {status}")


if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = ChatRoom_ui.Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", str(e))
