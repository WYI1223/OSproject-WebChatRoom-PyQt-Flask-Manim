@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    send(message, broadcast=True)