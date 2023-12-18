from datetime import datetime
from bson.json_util import dumps
from flask import Flask, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages
from flask_socketio import SocketIO
#netstat -ano | find "5000"
##taskkill /F /PID <process_id>


app = Flask(__name__)
app.secret_key = "sfdjkafnk"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 用户加载函数，用于从数据库中加载用户
@login_manager.user_loader
def load_user(username):
    return get_user(username)


# 处理 SocketIO 连接事件
@socketio.on('connect')
def handle_connect():
    # 如果用户已经通过身份验证，获取用户的聊天室并发送给客户端
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
        socketio.emit('update_rooms', {'rooms': rooms})


# 处理 SocketIO 登录事件
@socketio.on('login')
def handle_login(data):
    username = data['username']
    password_input = data['password']
    user = get_user(username)

    # 验证用户登录
    if user and user.check_password(password_input):
        login_user(user)
        rooms = get_rooms_for_user(username)
        socketio.emit('login_response', {'success': True, 'rooms': rooms})
    else:
        socketio.emit('login_response', {'success': False, 'message': 'Failed to login'})


# 处理 SocketIO 注册事件
@socketio.on('signup')
def handle_signup(data):
    username = data['username']
    email = data['email']
    password = data['password']

    # 保存新用户，处理重复键错误
    try:
        save_user(username, email, password)
        socketio.emit('signup_response', {'success': True})
    except KeyError:
        socketio.emit('signup_response', {'success': False, 'message': 'User already exists!'})


# 处理 SocketIO 创建聊天室事件
@socketio.on('create_room')
@login_required
def handle_create_room(data):
    room_name = data['room_name']
    usernames = [username.strip() for username in data['members'].split(',')]

    # 尝试创建新聊天室，处理错误
    if len(room_name) and len(usernames):
        try:
            room_id = save_room(room_name, current_user.username)
            if current_user.username in usernames:
                usernames.remove(current_user.username)
            add_room_members(room_id, room_name, usernames, current_user.username)
            socketio.emit('create_room_response', {'success': True, 'room_id': room_id})
        except KeyError:
            socketio.emit('create_room_response', {'success': False, 'message': 'Failed to create room'})
    else:
        socketio.emit('create_room_response', {'success': False, 'message': 'Failed to create room'})


# 处理 SocketIO 编辑聊天室事件
@socketio.on('edit_room')
@login_required
def handle_edit_room(data):
    room_id = data['room_id']
    room = get_room(room_id)

    # 如果聊天室存在且当前用户是管理员
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member.username for member in get_room_members(room_id)]
        room_members = [username.strip() for username in data['members'].split(',')]

        room_name = data['room_name']
        room['name'] = room_name
        update_room(room_id, room_name)

        members_to_add = list(set(room_members) - set(existing_room_members))
        members_to_remove = list(set(existing_room_members) - set(room_members))

        # 添加和移除聊天室成员
        if len(members_to_add):
            add_room_members(room_id, room_name, members_to_add, current_user.username)
        if len(members_to_remove):
            remove_room_members(room_id, members_to_remove)

        socketio.emit('edit_room_response', {'success': True, 'room_members': room_members})
    else:
        socketio.emit('edit_room_response', {'success': False, 'message': 'Room not found or permission denied'})


# 处理 SocketIO 查看聊天室事件
@socketio.on('view_room')
@login_required
def handle_view_room(data):
    room_id = data['room_id']
    room = get_room(room_id)

    # 如果聊天室存在且当前用户是成员
    if room and is_room_member(room_id, current_user.username):
        room_members = [member.username for member in get_room_members(room_id)]
        messages = get_messages(room_id)
        socketio.emit('view_room_response', {'success': True, 'username': current_user.username,
                                             'room': room, 'room_members': room_members, 'messages': messages})
    else:
        socketio.emit('view_room_response', {'success': False, 'message': 'Room not found or permission denied'})


# 处理 SocketIO 获取旧消息事件
@socketio.on('get_older_messages')
@login_required
def handle_get_older_messages(data):
    room_id = data['room_id']
    room = get_room(room_id)

    # 如果聊天室存在且当前用户是成员
    if room and is_room_member(room_id, current_user.username):
        page = int(data.get('page', 0))
        messages = get_messages(room_id, page)
        socketio.emit('get_older_messages_response', {'messages': messages})
    else:
        socketio.emit('get_older_messages_response', {'message': 'Room not found or permission denied'})


# 处理 SocketIO 发送消息事件
@socketio.on('send_message')
@login_required
def handle_send_message_event(data):
    # 记录日志
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    # 添加消息的创建时间
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    # 保存消息到数据库
    save_message(data['room'], data['message'], data['username'])
    # 向房间内的所有成员发送消息
    socketio.emit('receive_message', data, room=data['room'])


# 处理 SocketIO 加入聊天室事件
@socketio.on('join_room')
@login_required
def handle_join_room_event(data):
    # 记录日志
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    # 加入聊天室
    join_room(data['room'])
    # 向聊天室内的所有成员发送加入通知
    socketio.emit('join_room_announcement', data, room=data['room'])


# 处理 SocketIO 离开聊天室事件
@socketio.on('leave_room')
@login_required
def handle_leave_room_event(data):
    # 记录日志
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    # 离开聊天室
    leave_room(data['room'])
    # 向聊天室内的所有成员发送离开通知
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
