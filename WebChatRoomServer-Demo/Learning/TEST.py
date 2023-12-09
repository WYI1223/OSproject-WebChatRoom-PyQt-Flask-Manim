from DISK import diskSim
from Memory import memorySim, virtualMemorySim
from flask import Flask, render_template, request
from flask_socketio import SocketIO


class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")


        # 绑定路由和事件处理函数
        self.app.route('/')(self.index)
        self.socketio.on('connect')(self.handle_connect)
        self.socketio.on('disconnect')(self.handle_disconnect)
        self.socketio.on('message')(self.handle_message)

        # 初始化服务器内存以及硬盘
        self.online_users = set()
        # self.memoryScheduler = Memory.memoryScheduler("server1", 100)
        self.diskSim = diskSim.diskSim("server1")
        self.virtualMemorySim = virtualMemorySim.virtualMemorySim("server1")
        self.memorySim = memorySim.memorySim(100)

        # 储存聊天记录 [(time,data),(time,data),(time,data)]
        self.record = []

    def index(self):
        return render_template('chat.html')

    def handle_connect(self):
        user_id = request.sid
        self.online_users.add(user_id)
        self.update_online_users()
        self.socketio.sleep(0.5)
        self.socketio.emit('message_record', self.record, room=user_id)

    def handle_disconnect(self):
        user_id = request.sid
        self.online_users.discard(user_id)
        self.update_online_users()

    def update_online_users(self):
        self.socketio.emit('online_users', list(self.online_users))

    def handle_message(self, data):
        self.socketio.emit('receive_message', data)
        self.record.append(data)

    def run(self):
        self.socketio.run(self.app, debug=True, allow_unsafe_werkzeug=True)


if __name__ == '__main__':
    chat_app = ChatApp()
    chat_app.run()
