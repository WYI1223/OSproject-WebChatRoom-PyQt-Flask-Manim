import threading

from PyQt5.QtWidgets import QMainWindow, QApplication
from qtChat import Ui_MainWindow
import sys

import socketio

class myChat(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.socketio = socketio.Client()
        self.socketio.connect('http://localhost:5000')

        # 按钮绑定事件
        self.send_button.clicked.connect(self.send_message)
        self.login_button.clicked.connect(self.login)
        self.signup_button.clicked.connect(self.signup)
        #  socketio绑定事件
        self.socketio.on('receive_message', self.receive_message)




    def receive_message(self, data):
        self.message_recv.addItem(data)

    def send_message(self):
        text = self.message_input.toPlainText()
        self.socketio.emit('message', text)
        self.message_recv.addItem(text)
        self.message_input.clear()

    def login(self):
        pass

    def signup(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mychat = myChat()
    mychat.show()
    sys.exit(app.exec_())
