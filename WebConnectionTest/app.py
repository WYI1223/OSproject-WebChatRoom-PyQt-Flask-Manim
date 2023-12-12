from flask import Flask, render_template, request  # 导入 Flask 和用于渲染模板的函数
from flask_socketio import SocketIO  # 导入 Flask-SocketIO

app = Flask(__name__)  # 创建一个 Flask 应用实例
app.config['SECRET_KEY'] = 'your_secret_key'  # 设置应用的密钥，用于会话等的安全性
socketio = SocketIO(app, cors_allowed_origins="*")  # 创建一个 SocketIO 实例，并与 Flask 应用关联

# 用于存储在线用户的集合
online_users = set()  # 创建一个集合用于存储在线用户的标识

@app.route('/')  # 定义路由：当用户访问网站根目录时
def index():
    return render_template('index.html')  # 返回 chat.html 模板的内容

@socketio.on('connect')  # 定义当有新的 WebSocket 连接时的处理逻辑
def handle_connect():
    user_id = request.sid  # 获取连接的用户的会话ID作为用户标识
    online_users.add(user_id)  # 将该用户添加到在线用户集合中
    update_online_users()  # 更新在线用户列表

@socketio.on('disconnect')  # 定义当有 WebSocket 断开连接时的处理逻辑
def handle_disconnect():
    user_id = request.sid  # 获取断开连接的用户的会话ID
    online_users.discard(user_id)  # 从在线用户集合中移除该用户
    update_online_users()  # 更新在线用户列表

def update_online_users():
    # 广播在线用户列表给所有连接的客户端
    socketio.emit('online_users', list(online_users))

@socketio.on('message')  # 定义当服务器接收到消息时的处理逻辑
def handle_message(data):
    # 这里可以添加消息处理逻辑
    socketio.emit('receive_message', data)  # 将接收到的消息广播给所有连接的客户端

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
