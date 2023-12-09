import threading

# 模拟内存
class MemorySim:
    def __init__(self):
        self.data = {}  # 存储内存中的数据

    def get_data(self, key):
        return self.data.get(key, None)

    def set_data(self, key, value):
        self.data[key] = value

# 模拟虚拟内存
class VirtualMemorySim:
    def __init__(self):
        self.data = {}  # 存储虚拟内存中的数据

    def get_data(self, key):
        return self.data.get(key, None)

    def set_data(self, key, value):
        self.data[key] = value

# 内存调度器
class MemoryScheduler:
    def __init__(self, memory, virtual_memory):
        self.memory = memory
        self.virtual_memory = virtual_memory
        self.lock = threading.Lock()

    def request_data(self, key):
        self.lock.acquire()  # 显式获取锁
        try:
            data = self.memory.get_data(key)
            if data is None:
                data = self.virtual_memory.get_data(key)
                if data is not None:
                    self.memory.set_data(key, data)
            return data
        finally:
            self.lock.release()  # 确保释放锁

class ThreadScheduler:
    def __init__(self, memory_scheduler):
        self.memory_scheduler = memory_scheduler
        self.threads = []

    def create_thread(self, target, args):
        thread = threading.Thread(target=target, args=args)
        self.threads.append(thread)

    def start_all_threads(self):
        for thread in self.threads:
            thread.start()

    def wait_all_threads(self):
        for thread in self.threads:
            thread.join()

# 线程函数
def chat_thread_function(pid, memory_scheduler, data_key):
    print(f"Thread {pid} starting")
    data = memory_scheduler.request_data(data_key)
    if data:
        print(f"Thread {pid} received data: {data}")
    else:
        print(f"Thread {pid} no data available")

# 初始化
memory = MemorySim()
virtual_memory = VirtualMemorySim()
memory_scheduler = MemoryScheduler(memory, virtual_memory)

# 假设聊天数据和其他数据被存储在虚拟内存中
virtual_memory.set_data("chat_data", "Hello from Virtual Memory!")
virtual_memory.set_data("other_data", "Some other information")

# 创建线程调度器
thread_scheduler = ThreadScheduler(memory_scheduler)

# 创建并添加线程
for i in range(5):
    thread_scheduler.create_thread(chat_thread_function, (i, memory_scheduler, "chat_data"))

# 启动并等待所有线程完成
thread_scheduler.start_all_threads()
thread_scheduler.wait_all_threads()

print("All threads have finished.")