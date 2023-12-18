import queue
import threading
import time

from Memory import diskSim, memorySim, virtualMemorySim ,memorySchedule
from flask import Flask, render_template, request
from flask_socketio import SocketIO


class ChatApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'your_secret_key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        self.users = {'user_id': 'password'}
        self.users_id = {'user_id': 'user_name'}

        # 绑定路由和事件处理函数
        self.app.route('/')(self.index)
        self.socketio.on('connect')(self.handle_connect)
        self.socketio.on('Label')(self.changeLabel)
        self.socketio.on('disconnect')(self.handle_disconnect)
        self.socketio.on('message')(self.handle_message)
        # self.socketio.on('threads_info_request')(self.handle_threads_info_request)

        # 初始化服务器内存以及硬盘
        self.diskSim = diskSim.diskSim("server1")
        self.diskSim._mkdir("server1", "root")
        self.diskSim._mkdir("record", "root/server1")

        self.memoryScheduler = memorySchedule.memoryScheduler("server1", 10, self.diskSim)

        # 在线用户列表 mid:online_users
        self.memoryScheduler._write("online_users", set())


        # 储存聊天记录 [(time,data),(time,data),(time,data)]
        self.history_message=[]

        # 共享锁
        self.mutex = threading.Lock()
        # 服务器日志
        self.log_condition = threading.Condition(self.mutex)
        self.log = queue.LifoQueue()
        self.savelog()

    def index(self):
        return render_template('chat.html')
    def savelog(self):
        log_thread = threading.Thread(target=self.savelogqueue,name="savelog")
        log_thread.start()



    def changeLabel(self,data):
        user_id = request.sid
        if data == None:
            connect_threads = threading.Thread(target=self.connect_threads,args=(user_id,"admin"), name=("connect_threads:" + user_id))
            connect_threads.start()
              #更新线程信息
            self.handle_threads_info_request()
            return
        username = data[0]
        password = data[1]
        state = data[2]

        if state == "login":
            if username in self.users and password == self.users[username]:
                self.socketio.emit('system_info', "Login successful ", room=user_id)
                self.users_id.update({user_id: username})
                self.socketio.emit('message_record',self.history_message)
            else:
                self.socketio.emit('system_info', "Check your username or password. Or sign up", room=user_id)
                return
            connect_threads = threading.Thread(target=self.connect_threads, args=(user_id, username),
                                               name=("connect_threads:" + user_id))
            connect_threads.start()
            self.handle_threads_info_request()

        if state == "signup":
            if username in self.users:
                self.socketio.emit('system_info', "User have signed up", room=user_id)
            else:
                self.users.update({username: password})
                self.socketio.emit('system_info', "Signup successfully", room=user_id)
                return
            
    def savelogqueue(self):
        while True:
            with self.log_condition:
                self.log_condition.wait()  # 等待有日志记录时被唤醒
                while not self.log.empty():
                    log = self.log.get()
                    with open("log.txt", "a") as f:
                        f.write(log + "\n")


    def handle_connect(self, ):
            user_id = request.sid
            connect_threads = threading.Thread(target=self.connect_threads,args=(user_id,"admin"), name=("connect_threads:" + user_id))
            connect_threads.start()
            # 更新线程信息
            self.handle_threads_info_request()



    def connect_threads(self,user_id,username):
        # 为每个用户创建一个线程，用于处理用户的连接请求，防止阻塞主线程。

        self.mutex.acquire()
        # 读取内存中的在线用户列表，将新用户添加到列表中，并更新在线用户列表。
        # self.users_online.append(username) # 将用户名添加到在线用户名列表

        online_users = self.memoryScheduler._read("online_users")
        online_users.add(user_id)
        self.memoryScheduler._update("online_users", online_users)

        self.log.put("RunningInfo: " + "user_id: " + user_id + " connected.")
        self.log_condition.notify()
        self.mutex.release()
        self.update_online_users()
        time.sleep(0.5)
        # 发送聊天记录
        record = self.memoryScheduler._read("record")
        with self.mutex:
            self.socketio.emit('message_record', record, room=user_id)
    def handle_disconnect(self):
        user_id = request.sid
        self.users_id.pop(user_id)
        disconnect_threads = threading.Thread(target=self.disconnect_threads,args=(user_id,), name=("disconnect_threads:" + user_id))
        disconnect_threads.start()
        # 更新线程信息
        self.handle_threads_info_request()
    def disconnect_threads(self,user_id):
        # 当用户断开连接时，从在线用户列表中删除该用户，并更新在线用户列表。

        self.mutex.acquire()
        # 读取内存中的在线用户列表，删除该用户，并更新在线用户列表。
        online_users = self.memoryScheduler._read("online_users")
        online_users.discard(user_id)
        self.memoryScheduler._update("online_users", online_users)

        self.log.put("RunningInfo: "+"user_id: " + user_id + " disconnected.")
        self.log_condition.notify()
        self.mutex.release()
        self.update_online_users()

    def update_online_users(self):
        with self.mutex:
            # online_users = self.memoryScheduler._read("online_users")
            self.socketio.emit('online_users', list(self.users_id.values()))


    def handle_message(self, data):
        user_id = request.sid
        if user_id not in self.users_id:
            self.socketio.emit('system_info',"You need to login then to send message!")
            return
        user_name = self.users_id[user_id]
        data = user_name+": "+data
        with self.mutex:
            self.socketio.emit('receive_message', data)

        self.history_message.append(data)
        # recard = self.memoryScheduler._read("record")
        # recard.append(data)
        # self.memoryScheduler._update("record", recard)

        with self.mutex:
            self.log.put("Message received: " + str(data))
            self.log_condition.notify()  # 通知日志线程有新日志

    def start_thread_info_loop(self):
        """
        在后台线程中启动一个循环，定期发送线程信息给所有客户端。
        """
        def loop():
            while True:
                threads_info = self.get_threads_info()
                self.socketio.emit('threads_info', threads_info)
                time.sleep(1)  # 每1秒发送一次

        thread = threading.Thread(target=loop,name="thread_info_loop")
        thread.daemon = True  # 设置为守护线程，这样当主程序退出时，这个线程也会退出
        thread.start()

    def start_memory_info_loop(self):
        """
        在后台线程中启动一个循环，定期发送内存信息给所有客户端。
        """
        def loop():
            while True:
                memory_info = []
                for i in self.memoryScheduler._getstate():
                    memory_info.append(str(i))
                self.socketio.emit('memory_info', memory_info)
                time.sleep(1)  # 每1秒发送一次
        thread = threading.Thread(target=loop, name="memory_info_loop")
        thread.daemon = True  # 设置为守护线程，这样当主程序退出时，这个线程也会退出
        thread.start()

    def get_threads_info(self):
        """
        获取当前活动的线程信息。
        """
        threads_info = []
        for thread in threading.enumerate():
            info = {
                'name': thread.name,
                'is_alive': thread.is_alive(),
                'daemon': thread.daemon
            }
            threads_info.append(info)
        return threads_info


    def handle_threads_info_request(self):
        """
        SocketIO 事件处理函数，发送当前活动线程的信息给客户端。
        """
        threads_info = self.get_threads_info()
        self.socketio.emit('threads_info', threads_info)

    def run(self):
        self.start_memory_info_loop()
        self.start_thread_info_loop()
        self.socketio.run(self.app, debug=True, allow_unsafe_werkzeug=True, port=8080)


if __name__ == '__main__':
    chat_app = ChatApp()
    chat_app.run()
