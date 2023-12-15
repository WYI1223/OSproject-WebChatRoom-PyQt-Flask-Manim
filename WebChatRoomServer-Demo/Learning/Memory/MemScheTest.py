import unittest
import diskSim
import threading

# 导入之前定义的 memoryScheduler 类
from memorySchedule import memoryScheduler  # 假设这个类在 your_module 模块中定义

class TestMemoryScheduler(unittest.TestCase):
    def setUp(self):
        self.disk = diskSim.diskSim("serverTest")
        self.disk.initialize_system_enhanced()
        self.disk._mkdir("serverTest", "root")
        self.memory_scheduler = memoryScheduler("serverTest", 10, self.disk)

    # 测试写入功能
    def test_write(self):
        result = self.memory_scheduler._write("1", "data1")
        self.assertTrue(result)
        self.assertEqual(self.memory_scheduler._read("1"), "data1")

    # 测试读取功能
    def test_read(self):
        self.memory_scheduler._write("2", "data2")
        result = self.memory_scheduler._read("2")
        self.assertEqual(result, "data2")

    # 测试更新功能
    def test_update(self):
        self.memory_scheduler._write("3", "data3")
        self.memory_scheduler._update("3", "new_data3")
        result = self.memory_scheduler._read("3")
        self.assertEqual(result, "new_data3")

    # 测试释放功能
    def test_release(self):
        self.memory_scheduler._write("4", "data4")
        self.memory_scheduler._release("4")
        result = self.memory_scheduler._read("4")
        self.assertIsNone(result)

    # 测试LRU算法的有效性
    def test_lru_algorithm(self):
        for i in range(1, 12):  # 写入超出内存容量的数据
            self.memory_scheduler._write(str(i), f"data{i}")

        # 检查是否最早的数据已被移动到虚拟内存
        self.assertIsNone(self.memory_scheduler._read("1"))
        self.assertIsNotNone(self.memory_scheduler._read("11"))

    # 测试多线程环境
    def test_multithreading(self):
        def write_data(id):
            for i in range(5):
                self.memory_scheduler._write(f"{id}-{i}", f"data{id}-{i}")

        threads = []
        for i in range(3):  # 创建3个线程
            thread = threading.Thread(target=write_data, args=(i,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # 检查数据是否正确写入
        for i in range(3):
            for j in range(5):
                result = self.memory_scheduler._read(f"{i}-{j}")
                self.assertEqual(result, f"data{i}-{j}")

if __name__ == '__main__':
    unittest.main()
