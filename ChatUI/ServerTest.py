# server.py

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
import sys
import threading

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 创建全局变量用于存储主窗口的引用
main_window = None

# 创建 Flask 的线程用于启动 Flask 服务
def run_flask():
    socketio.run(app, debug=True)

# 创建 Qt 的线程用于显示 Qt 界面
def run_qt():
    app = QApplication(sys.argv)
    global main_window
    main_window = QMainWindow()
    web_view = QWebEngineView(main_window)
    web_view.load(QUrl("http://127.0.0.1:5000"))
    main_window.setCentralWidget(web_view)
    main_window.show()
    sys.exit(app.exec_())

@app.route('/')
def index():
    return render_template('index.html')  # 用于显示 Qt 界面的 HTML 文件

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message_from_ui')
def handle_message(data):
    print('Received message from UI:', data)
    emit('message_from_server', {'response': 'Message received from server'})

if __name__ == '__main__':
    # 启动 Flask 线程
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # 启动 Qt 线程
    qt_thread = threading.Thread(target=run_qt)
    qt_thread.start()
