import threading
import time
from . import memorySim
from . import virtualMemorySim
from . import diskSim



# 内存调度器
# LRU调度算法
# _write(mid, data) 写入数据
# _read(mid) 读取数据
# _update(mid, data) 更新数据
# _release(mid) 释放数据
# _getstate() 返回内存状态


class memoryScheduler:

    def __init__(self, serverName, length, disk:diskSim):
        # 初始化内存，以及虚拟内存
        self.memory = memorySim.memorySim(length)
        self.disk = disk.delete("root/"+serverName+"/VirtualMemory")
        self.vmemory = virtualMemorySim.virtualMemorySim(serverName,disk)
        # table储存每个内存上次被访问的时间
        # counter用来计数
        self.counter = 0
        self.table = {}
        # 用于记录处于虚拟内存中的数据
        self.vmemoryTable = []

    def _write(self, mid, data):
        if mid in self.table:
            print("Error: memoryScheduler._create: mid already exists", mid)
            return False
        if self.memory.add(mid, data):
            self.table[mid] = self.counter
            self.counter += 1
            return True
        else:
            # 内存已满，将最早访问的数据转移到虚拟内存中
            self._Mem2Vmem(self.find_last_access_early())
            # 将数据写入内存
            if self.memory.add(mid, data):
                self.table[mid] = self.counter
                self.counter += 1
                return True

    def _read(self, mid):
        if mid not in self.table:
            if mid not in self.vmemoryTable:
                print("Error: memoryScheduler._read: mid not exists", mid)
                return None
            else:
                # 将最早访问的数据转移到虚拟内存中
                self._Mem2Vmem(self.find_last_access_early())
                # 将数据写入内存
                self._Vmem2Mem(mid)
                # 返回数据
                return self.memory.get(mid)
        else:
            self.table[mid] = self.counter
            self.counter += 1
            return self.memory.get(mid)

    def find_last_access_early(self):
        last_access_time = self.counter
        last_access_mid = None
        for mid in self.table:
            if self.table[mid] < last_access_time:
                last_access_time = self.table[mid]
                last_access_mid = mid
        return last_access_mid

    def _Mem2Vmem(self, mid):
        print("Mem2Vmem", mid)
        # 将内存中的数据转移到虚拟内存中
        data = self.memory.get(mid)
        self.vmemory.write(mid, data)
        self.memory.delete(mid)
        self.table.pop(mid)
        self.vmemoryTable.append(mid)

    def _Vmem2Mem(self, mid):
        print("Vmem2Mem", mid)
        # 将虚拟内存中的数据转移到内存中
        data = self.vmemory.read(mid)
        self.memory.add(mid, data)
        self.vmemory.delete(mid)
        self.vmemoryTable.remove(mid)
        self.table[mid] = self.counter
        self.counter += 1


    def _update(self, mid, data):
        if mid not in self.table:
            if mid not in self.vmemoryTable:
                print("Error: memoryScheduler._update: mid not exists", mid)
                return False
            else:
                # 将最早访问的数据转移到虚拟内存中
                self._Mem2Vmem(self.find_last_access_early())
                # 将数据写入内存
                self._Vmem2Mem(mid)
                self.memory.change(mid, data)
                # 返回数据
                return True
        else:
            self.table[mid] = self.counter
            self.counter += 1
            self.memory.change(mid, data)
            return True

    def _release(self, mid):
        if mid not in self.table:
            if mid not in self.vmemoryTable:
                return True
            else:
                self.vmemoryTable.remove(mid)
                self.vmemory.delete(mid)
        else:
            self.table.pop(mid)
            self.memory.delete(mid)


    def _getstate(self):
        return "Memory:", self.memory.__str__(), "Vmemory", self.vmemory.getTable(), \
               "MemoryScheduler:", self.table, self.vmemoryTable

#
# if __name__ == "__main__":
#     def getstate(memoryscheduler):
#         while(True):
#             print(memoryscheduler._getstate())
#             # time.sleep(0.5)
#
#     def writeCycle(memoryscheduler):
#         i = 0
#         while(True):
#             i += 1
#             memoryscheduler._write(str(i),str(i))
#             print("write", i)
#             # time.sleep(0.5)
#     def readCycle(memoryscheduler):
#         j = 0
#         while(True):
#             j += 1
#             print("read", str(j), memoryscheduler._read(str(j)))
#             # time.sleep(0.5)
#
#     def deleteCycle(memoryscheduler):
#         k = 0
#         while(True):
#             k += 1
#             memoryscheduler._release(str(k))
#             print("delete", str(k))
#             # time.sleep(0.5)
#
#     diskSim = diskSim.diskSim("server1")
#     diskSim.initialize_system_enhanced()
#     diskSim._mkdir("server1", "root")
#     memoryScheduler = memoryScheduler("server1", 10, diskSim)
#     t1 = threading.Thread(target=getstate, args=(memoryScheduler,))
#     t2 = threading.Thread(target=writeCycle, args=(memoryScheduler,))
#     t3 = threading.Thread(target=readCycle, args=(memoryScheduler,))
#     t4 = threading.Thread(target=deleteCycle, args=(memoryScheduler,))
#     t1.start()
#     t2.start()
#     time.sleep(1)
#     t3.start()
#     time.sleep(1)
#     t4.start()
