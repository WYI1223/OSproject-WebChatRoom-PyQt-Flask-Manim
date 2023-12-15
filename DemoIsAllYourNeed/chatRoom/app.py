from datetime import datetime
from bson.json_util import dumps
from flask import Flask, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, join_room, leave_room
from pymongo.errors import DuplicateKeyError
from db import get_user, save_user, save_room, add_room_members, get_rooms_for_user, get_room, is_room_member, \
    get_room_members, is_room_admin, update_room, remove_room_members, save_message, get_messages

app = Flask(__name__)
app.secret_key = "sfdjkafnk"
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    return get_user(username)


@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        rooms = get_rooms_for_user(current_user.username)
        socketio.emit('update_rooms', {'rooms': rooms})


@socketio.on('login')
def handle_login(data):
    username = data['username']
    password_input = data['password']
    user = get_user(username)

    if user and user.check_password(password_input):
        login_user(user)
        rooms = get_rooms_for_user(username)
        socketio.emit('login_response', {'success': True, 'rooms': rooms})
    else:
        socketio.emit('login_response', {'success': False, 'message': 'Failed to login'})


@socketio.on('signup')
def handle_signup(data):
    username = data['username']
    email = data['email']
    password = data['password']

    try:
        save_user(username, email, password)
        socketio.emit('signup_response', {'success': True})
    except DuplicateKeyError:
        socketio.emit('signup_response', {'success': False, 'message': 'User already exists!'})


@socketio.on('create_room')
@login_required
def handle_create_room(data):
    room_name = data['room_name']
    usernames = [username.strip() for username in data['members'].split(',')]

    if len(room_name) and len(usernames):
        room_id = save_room(room_name, current_user.username)
        if current_user.username in usernames:
            usernames.remove(current_user.username)
        add_room_members(room_id, room_name, usernames, current_user.username)
        socketio.emit('create_room_response', {'success': True, 'room_id': room_id})
    else:
        socketio.emit('create_room_response', {'success': False, 'message': 'Failed to create room'})


@socketio.on('edit_room')
@login_required
def handle_edit_room(data):
    room_id = data['room_id']
    room = get_room(room_id)
    if room and is_room_admin(room_id, current_user.username):
        existing_room_members = [member.username for member in get_room_members(room_id)]
        room_members = [username.strip() for username in data['members'].split(',')]

        room_name = data['room_name']
        room['name'] = room_name
        update_room(room_id, room_name)

        members_to_add = list(set(room_members) - set(existing_room_members))
        members_to_remove = list(set(existing_room_members) - set(room_members))
        if len(members_to_add):
            add_room_members(room_id, room_name, members_to_add, current_user.username)
        if len(members_to_remove):
            remove_room_members(room_id, members_to_remove)

        socketio.emit('edit_room_response', {'success': True, 'room_members': room_members})
    else:
        socketio.emit('edit_room_response', {'success': False, 'message': 'Room not found or permission denied'})


@socketio.on('view_room')
@login_required
def handle_view_room(data):
    room_id = data['room_id']
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        room_members = [member.username for member in get_room_members(room_id)]
        messages = get_messages(room_id)
        socketio.emit('view_room_response', {'success': True, 'username': current_user.username,
                                             'room': room, 'room_members': room_members, 'messages': messages})
    else:
        socketio.emit('view_room_response', {'success': False, 'message': 'Room not found or permission denied'})


@socketio.on('get_older_messages')
@login_required
def handle_get_older_messages(data):
    room_id = data['room_id']
    room = get_room(room_id)
    if room and is_room_member(room_id, current_user.username):
        page = int(data.get('page', 0))
        messages = get_messages(room_id, page)
        socketio.emit('get_older_messages_response', {'messages': messages})
    else:
        socketio.emit('get_older_messages_response', {'message': 'Room not found or permission denied'})


@socketio.on('send_message')
@login_required
def handle_send_message_event(data):
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    data['created_at'] = datetime.now().strftime("%d %b, %H:%M")
    save_message(data['room'], data['message'], data['username'])
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
@login_required
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
@login_required
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
