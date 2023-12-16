from PyQt5 import QtCore, QtGui, QtWidgets
import ChatRoom_ui
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from socketIO_client import SocketIO
class ChatClient(QtCore.QObject):
    messageReceived = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = SocketIO('', 5000)
        self.connect_signals()

    def connect_signals(self):
        self.socket.on('connect', self.handle_connect)
        self.socket.on('receive_message', self.handle_receive_message)

    def handle_connect(self):
        print("Connected to server")
        # You may emit additional signals or perform actions on connection

    def handle_receive_message(self, data):
        self.messageReceived.emit(data)

    def login(self, username, password):
        # Implement login logic here
        self.socket.emit('login', {'username': username, 'password': password})

    # Add other methods for signup, room creation, etc.
class MyMainWindow(QtWidgets.QMainWindow, ChatRoom_ui.Ui_MainWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)

        # Connect the Send button to the send_message function
        self.pushButton_6.clicked.connect(self.send_message)

        
        # Set up delegate for listWidget
        self.listWidget.setItemDelegate(ChatRoom_ui.BubbleDelegate())

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
            self.chat_client = ChatClient()
            self.chat_client.messageReceived.connect(self.handle_message_received)

            self.pushButton_6.clicked.connect(self.handle_send_message)
            self.pushButton_7.clicked.connect(self.handle_login)
            self.pushButton_8.clicked.connect(self.handle_signup)

    def handle_send_message(self):
        # Implement sending message logic
        username = self.textEdit_2.toPlainText()
        message = self.textEdit.toPlainText()
        room_id = 123  # Replace with the actual room ID
        self.chat_client.socket.emit('send_message', {'username': username, 'room': room_id, 'message': message})

    def handle_login(self):
        # Implement login logic
        username = self.textEdit_2.toPlainText()
        password = self.textEdit_3.toPlainText()
        self.chat_client.login(username, password)

    def add_message(self, text, user_role):
        item = QtWidgets.QListWidgetItem(text)
        item.setData(QtCore.Qt.UserRole, user_role)
        self.listWidget.addItem(item)

    def send_message(self):
        message_text = self.textEdit.toPlainText()
        if message_text:
            self.add_message(message_text, "outgoing")
            self.textEdit.clear()

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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ChatRoom_ui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())