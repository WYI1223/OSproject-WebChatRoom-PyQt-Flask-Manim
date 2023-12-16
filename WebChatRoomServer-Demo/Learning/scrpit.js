const socket = io('http://localhost:5000'); // 根据您的服务器配置更改端口

function login() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    socket.emit('login', { username, password });
}

function signup() {
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    socket.emit('signup', { username, email, password });
}

function sendMessage() {
    const message = document.getElementById('message-input').value;
    // 这里需要一个方式来获取当前的聊天室ID
    const room = 'some_room_id';
    socket.emit('send_message', { message, room });
}

socket.on('login_response', data => {
    if (data.success) {
        // 处理登录成功
    } else {
        // 处理登录失败
    }
});

socket.on('signup_response', data => {
    if (data.success) {
        // 处理注册成功
    } else {
        // 处理注册失败
    }
});

socket.on('receive_message', data => {
    // 显示接收到的消息
});
