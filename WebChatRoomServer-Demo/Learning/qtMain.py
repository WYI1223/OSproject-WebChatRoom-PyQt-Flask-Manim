import threading
import time

from PyQt5.QtWidgets import QMainWindow, QApplication
from qtChat import Ui_MainWindow
import sys

import socketio

class myChat(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.LabelConten = ("Login if you have acount, "
                            "\nsignup if you do not have a acount")
        self.label_2.setText(self.LabelConten)


        self.socketio = socketio.Client()
        self.socketio.connect('http://localhost:8080')

        # 按钮绑定事件
        self.send_button.clicked.connect(self.send_message)
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)


        #  socketio绑定事件
        self.socketio.on('receive_message', self.receive_message)
        self.socketio.on('online_users', self.update_online_users)
        self.socketio.on('message_record', self.recv_message_record)
        self.socketio.on('system_info',self.changeSystemInfo)
        self.username = None
    def update_online_users(self, data):
        time.sleep(1)
        self.listWidget_2.clear()
        for user in data:
            self.listWidget_2.addItem(user)

    # 更新系统信息提醒函数
    def changeSystemInfo(self, info):
        self.label_2.setText(info)
    def recv_message_record(self, data):
        if data is not None:
            for i in data:
                self.message_recv.addItem(data[i])
    def receive_message(self, data):
        self.message_recv.addItem(data)

    def send_message(self):
        text = self.message_input.toPlainText()
        self.socketio.emit('message', text)
        self.message_input.clear()





    def login(self):
        state = "login"
        self.username = self.username_input.toPlainText()
        self.password = self.password_input.toPlainText()
        data = [str(self.username),str(self.password),"login"]
        self.socketio.emit('Label',data)


    def signup(self):
        self.username = self.username_input.toPlainText()
        self.password = self.password_input.toPlainText()
        data = [str(self.username), str(self.password), "signup"]
        self.socketio.emit('Label', data)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mychat = myChat()
    mychat.show()
    sys.exit(app.exec_())
