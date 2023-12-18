import threading
import time

import logSystem
from Memory import diskSim, memorySim, virtualMemorySim, memorySchedule
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
        self.socketio.on('Label')(self.loginSystem)
        self.socketio.on('disconnect')(self.handle_disconnect)
        self.socketio.on('message')(self.handle_message)
        self.socketio.on('get_log')(self.get_log)
        # self.socketio.on('threads_info_request')(self.handle_threads_info_request)

        # 初始化服务器内存以及硬盘
        self.diskSim = diskSim.diskSim("server1")
        self.diskSim._mkdir("server1", "root")
        self.diskSim._mkdir("record", "root/server1")

        self.memoryScheduler = memorySchedule.memoryScheduler("server1", 10, self.diskSim)

        # 共享锁
        self.mutex = threading.Lock()

        # 在线用户列表 mid:online_users
        users = self.user_info()
        users_id = {'user_id': 'user_name'}
        self.memoryScheduler._write("user-pwd", users)
        self.memoryScheduler._write("user-id", users_id)

        # 储存聊天记录 [(time,data),(time,data),(time,data)]
        self.memoryScheduler._write("history_message", [])

        # 服务器日志
        self.logSystem = logSystem.logSystem(self.diskSim, "server1")
        self.logSystem.put("RunningInfo: " + "Server1 started.")
        self.logSystem.put("RunningInfo: " + "Server1 get user_info: " + str(self.user_info()))

    def index(self):
        return render_template('chat.html')

    def user_info(self):
        data = self.diskSim.read_file("root/" + "server1" + "/user_info")
        if data is False:
            self.diskSim.write_file("user_info", {'user_id': 'password'}, "root/" + "server1")
            return self.diskSim.read_file("root/" + "server1" + "/user_info")
        return eval(data)

    def get_log(self):
        user_id = request.sid
        self.socketio.emit('log', self.logSystem.get(), room=user_id)

    def loginSystem(self, data):

        # 模拟内存占用
        self.memoryScheduler._write("loginSystem", data)

        user_id = request.sid
        self.logSystem.put("RunningInfo: " + "user_id: " + user_id + " loginSystem: " + str(data))
        if data == None:
            connect_threads = threading.Thread(target=self.connect_threads, args=(user_id, "admin"),
                                               name=("connect_threads:" + user_id))
            connect_threads.start()
            # 更新线程信息
            self.handle_threads_info_request()

            # 模拟内存释放
            self.memoryScheduler._release("loginSystem")
            return

        username, password, state = data

        users = self.memoryScheduler._read("user-pwd")
        if state == "login":
            # 如果已登录，提示用户已登录
            if user_id in self.memoryScheduler._read("user-id"):
                self.socketio.emit('system_info', "You have already logged in", room=user_id)

                # 模拟内存释放
                self.memoryScheduler._release("loginSystem")
                return
            # 特权用户
            if username == "admin" and password == "admin":
                self.socketio.emit('system_info', "Login successful ", room=user_id)
                self.logSystem.put("RunningInfo: " + "user_id: " + user_id + " loginSystem: " + str(data))

                # 更新在线用户列表
                self.users_id = self.memoryScheduler._read("user-id")
                self.users_id.update({user_id: username})
                self.memoryScheduler._update("user-id", self.users_id)

                self.socketio.emit('message_record', self.memoryScheduler._read("history_message"), room=user_id)

                # 模拟内存释放
                self.memoryScheduler._release("loginSystem")
                return
            if username in users and password == users[username]:
                self.socketio.emit('system_info', "Login successful ", room=user_id)

                # 更新在线用户列表
                self.users_id = self.memoryScheduler._read("user-id")
                self.users_id.update({user_id: username})
                self.memoryScheduler._update("user-id", self.users_id)

                self.socketio.emit('message_record', self.memoryScheduler._read("history_message"), room=user_id)

            else:
                self.socketio.emit('system_info', "Check your username or password. Or sign up", room=user_id)
                # 模拟内存释放
                self.memoryScheduler._release("loginSystem")
                return
            connect_threads = threading.Thread(target=self.connect_threads, args=(user_id,),
                                               name=("connect_threads:" + user_id))
            connect_threads.start()
            self.handle_threads_info_request()
            # 模拟内存释放
            self.memoryScheduler._release("loginSystem")

        if state == "signup":
            if username in users:
                self.socketio.emit('system_info', "User have signed up", room=user_id)
                # 模拟内存释放
                self.memoryScheduler._release("loginSystem")
            else:
                # 新用户注册
                users.update({username: password})
                # 更新内存
                self.memoryScheduler._update("user-pwd", users)
                # 写入文件
                self.diskSim.delete("root/" + "server1" + "/user_info")
                self.diskSim.write_file("user_info", users, "root/" + "server1")
                self.logSystem.put("RunningInfo: " + "user_id: " + user_id + " loginSystem: " + str(data))
                self.socketio.emit('system_info', "Signup successfully", room=user_id)
                # 模拟内存释放
                self.memoryScheduler._release("loginSystem")
                return


    def handle_connect(self):
        user_id = request.sid
        connect_threads = threading.Thread(target=self.connect_threads, args=(user_id,),
                                           name=("connect_threads:" + user_id))
        connect_threads.start()
        # 更新线程信息
        self.handle_threads_info_request()

    def handle_disconnect(self):
        user_id = request.sid
        disconnect_threads = threading.Thread(target=self.disconnect_threads, args=(user_id,),
                                              name=("disconnect_threads:" + user_id))
        disconnect_threads.start()
        # 更新线程信息
        self.handle_threads_info_request()

    def connect_threads(self, user_id,):
        # 为每个用户创建一个线程，用于处理用户的连接请求，防止阻塞主线程。

        self.mutex.acquire()
        # self.log.put("RunningInfo: " + "user_id: " + user_id + " connected.")
        # self.log_condition.notify()
        self.mutex.release()
        self.update_online_users()
        time.sleep(0.5)
        # 发送聊天记录

    def disconnect_threads(self, user_id):
        # 当用户断开连接时，从在线用户列表中删除该用户，并更新在线用户列表。

        self.mutex.acquire()
        # 读取内存中的在线用户列表，删除该用户，并更新在线用户列表。
        online_users = self.memoryScheduler._read("user-id")
        online_users.pop(user_id)
        self.memoryScheduler._update("user-id", online_users)
        # self.log.put("RunningInfo: " + "user_id: " + user_id + " disconnected.")

        self.logSystem.put("RunningInfo: " + "user_id: " + user_id + " disconnected.")

        self.mutex.release()
        self.update_online_users()

    def update_online_users(self):
        with self.mutex:
            # online_users = self.memoryScheduler._read("online_users")
            self.socketio.emit('online_users', list(self.memoryScheduler._read("user-id").values()))

    def handle_message_threads(self, data, user_id):
        """
        为每个用户创建一个线程，用于处理用户的消息，防止阻塞主线程。并且为线程命名。
        """
        # 模拟内存占用
        self.memoryScheduler._write("handle_message_threads", data)

        self.logSystem.put("RunningInfo: " + "user_id: " + user_id + " send message: " + str(data))
        users_id = self.memoryScheduler._read("user-id")
        if user_id not in users_id:
            self.socketio.emit('system_info', "You need to login then to send message!", room=user_id)
            return
        user_name = users_id[user_id]

        data = user_name + ": " + data
        with self.mutex:
            self.socketio.emit('receive_message', data, room=list(self.memoryScheduler._read("user-id").keys()))

        # 更新聊天记录
        history_message = self.memoryScheduler._read("history_message")
        history_message.append(data)
        self.memoryScheduler._update("history_message", history_message)

        # with self.mutex:
            # self.log.put("Message received: " + str(data))
            # self.log_condition.notify()  # 通知日志线程有新日志

    def handle_message(self, data):
        user_id = request.sid
        thread = threading.Thread(target=self.handle_message_threads, args=(data, user_id),
                                  name=("handle_message_threads:" + data))
        thread.start()

    def start_thread_info_loop(self):
        """
        在后台线程中启动一个循环，定期发送线程信息给所有客户端。
        """

        def loop():
            while True:
                threads_info = self.get_threads_info()
                self.socketio.emit('threads_info', threads_info)
                time.sleep(1)  # 每1秒发送一次

        thread = threading.Thread(target=loop, name="thread_info_loop")
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
                time.sleep(0.5)  # 每1秒发送一次

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
