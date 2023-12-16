from datetime import datetime

from bson import ObjectId
from werkzeug.security import generate_password_hash

from user import User

from datetime import datetime

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class RoomMember:
    def __init__(self, room_id, room_name, username, added_by, is_room_admin=False):
        self.room_id = room_id
        self.room_name = room_name
        self.username = username
        self.added_by = added_by
        self.is_room_admin = is_room_admin

class Message:
    def __init__(self, room_id, text, sender, created_at):
        self.room_id = room_id
        self.text = text
        self.sender = sender
        self.created_at = created_at

# Mock database using dictionaries and lists
users_data = {}
rooms_data = {}
room_members_data = {}
messages_data = {}

def save_user(username, email, password):
    # 保存用户信息到 users_collection 集合
    password_hash = generate_password_hash(password)
    users_data[username] = User(username, email, password_hash)

def get_user(username):
    # 查询并返回指定用户名的用户信息
    return users_data.get(username)

def save_room(room_name, created_by):
    # 保存聊天室信息到 rooms_collection 集合，并调用 add_room_member 添加房间成员
    room_id = ObjectId()
    rooms_data[room_id] = {'name': room_name, 'created_by': created_by, 'created_at': datetime.now()}
    add_room_member(room_id, room_name, created_by, created_by, is_room_admin=True)
    return room_id

def update_room(room_id, room_name):
    # 更新房间名称，并同步更新 room_members_collection 中的房间名
    rooms_data[room_id]['name'] = room_name
    for member in room_members_data.values():
        if member.room_id == room_id:
            member.room_name = room_name

def get_room(room_id):
    # 查询并返回指定房间 ID 的房间信息
    return rooms_data.get(room_id)

def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
    # 添加房间成员信息到 room_members_collection 集合
    member_key = (room_id, username)
    room_members_data[member_key] = RoomMember(room_id, room_name, username, added_by, is_room_admin)

def add_room_members(room_id, room_name, usernames, added_by):
    # 批量添加房间成员信息到 room_members_collection 集合
    for username in usernames:
        add_room_member(room_id, room_name, username, added_by, is_room_admin=False)

def remove_room_members(room_id, usernames):
    # 移除指定房间 ID 和用户名的房间成员信息
    for username in usernames:
        member_key = (room_id, username)
        if member_key in room_members_data:
            del room_members_data[member_key]

def get_room_members(room_id):
    # 查询并返回指定房间 ID 的所有房间成员信息
    return [member for member in room_members_data.values() if member.room_id == room_id]

def get_rooms_for_user(username):
    # 查询并返回指定用户名的所有房间信息
    return [member.room_name for member in room_members_data.values() if member.username == username]

def is_room_member(room_id, username):
    # 判断指定房间 ID 和用户名的用户是否为房间成员
    member_key = (room_id, username)
    return member_key in room_members_data

def is_room_admin(room_id, username):
    # 判断指定房间 ID 和用户名的用户是否为房间管理员
    member_key = (room_id, username)
    member = room_members_data.get(member_key)
    return member and member.is_room_admin

def save_message(room_id, text, sender):
    # 保存消息到 messages_collection 集合
    message_id = ObjectId()
    messages_data[message_id] = Message(room_id, text, sender, datetime.now())

def get_messages(room_id, page=0):
    # 查询并返回指定房间 ID 的消息列表
    messages = [message for message in messages_data.values() if message.room_id == room_id]
    messages.sort(key=lambda m: m.created_at, reverse=True)
    offset = page * MESSAGE_FETCH_LIMIT
    return messages[offset:offset + MESSAGE_FETCH_LIMIT]

MESSAGE_FETCH_LIMIT = 3
