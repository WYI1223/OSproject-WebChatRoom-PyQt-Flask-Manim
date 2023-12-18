import queue
import threading
import time
import json

from Memory import diskSim

class logSystem:

    def __init__(self, disk:diskSim, serverName):

        self.disk = disk
        self.serverName = serverName
        self.disk._mkdir("log", "root/"+serverName)
        self.logloc = "root/"+serverName+"/log"
        self.num = self.disk.read_file(self.logloc+"/num")

        self.mutex = threading.Lock()
        self.log_condition = threading.Condition(self.mutex)
        self.log = queue.LifoQueue()
        self.save_log()


    def save_log(self):
        log_thread = threading.Thread(target=self.save_log_queue,name="save_log",daemon=True)
        log_thread.start()

    def save_log_queue(self):
        while True:
            with self.log_condition:
                self.log_condition.wait()
                while not self.log.empty():
                    log = self.log.get()

                    # 尝试读取旧的日志文件
                    old_log_content = self.disk.read_file(self.logloc + "/log")
                    if old_log_content:
                        try:
                            # 尝试将读取的内容解析为JSON格式的列表
                            old_log = json.loads(old_log_content)
                        except json.JSONDecodeError:
                            # 如果解析失败，就将old_log设置为空列表
                            print("Error: logSystem.save_log_queue: JSONDecodeError")
                            # old_log = []
                    else:
                        old_log = []

                    # 将新日志添加到列表中
                    old_log.append(log)

                    # 将更新后的日志列表保存到文件中
                    self.disk.delete(self.logloc + "/log")
                    self.disk.write_file("log", json.dumps(old_log), self.logloc)


    def put(self, log):
        with self.mutex:
            self.log.put(log +" at " + str(time.time()))
            self.log_condition.notify()


    def get(self):
        text = self.disk.read_file(self.logloc+"/log")
        print(text)
        return json.loads(text)
