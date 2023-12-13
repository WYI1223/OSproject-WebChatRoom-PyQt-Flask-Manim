import time
import memorySim
import virtualMemorySim
import diskSim

class memoryScheduler:

    def __init__(self, serverName, length, disk:diskSim):
        # 初始化内存，以及虚拟内存
        self.memory = memorySim.memorySim(length)
        self.vmemory = virtualMemorySim.virtualMemorySim(serverName,disk)
        # table储存每个内存上次被访问的时间
        self.table = {}
        # 用于记录处于虚拟内存中的数据
        self.vmemoryTable = []
    def _write(self, mid, data):
        if mid in self.table:
            print("Error: memoryScheduler._create: mid already exists")
            return False
        if self.memory.add(mid, data):
            self.table[mid] = time.time()
            return True
        else:
            # 内存已满，将最早访问的数据转移到虚拟内存中
            self._Mem2Vmem(self.find_last_access_early())
            # 将数据写入内存
            if self.memory.add(mid, data):
                self.table[mid] = time.time()
                return True

    def _read(self, mid):
        if mid not in self.table:
            if mid not in self.vmemoryTable:
                print("Error: memoryScheduler._read: mid not exists")
                return None
            else:
                # 将最早访问的数据转移到虚拟内存中
                self._Mem2Vmem(self.find_last_access_early())
                # 将数据写入内存
                self._Vmem2Mem(mid)
                # 返回数据
                return self.memory.get(mid)
        else:
            self.table[mid] = time.time()
            return self.memory.get(mid)

    def find_last_access_early(self):
        last_access_time = time.time()
        last_access_mid = None
        for mid in self.table:
            if self.table[mid] < last_access_time:
                last_access_time = self.table[mid]
                last_access_mid = mid
        return last_access_mid

    def _Mem2Vmem(self, mid):
        # 将内存中的数据转移到虚拟内存中
        data = self.memory.get(mid)
        self.vmemory.write(mid, data)
        self.memory.delete(mid)
        self.table.pop(mid)
        self.vmemoryTable.append(mid)

    def _Vmem2Mem(self, mid):
        # 将虚拟内存中的数据转移到内存中
        data = self.vmemory.read(mid)
        self.memory.write(mid, data)
        self.vmemory.delete(mid)
        self.vmemoryTable.remove(mid)
        self.table[mid] = time.time()


    def _update(self, mid, data):
        if mid not in self.table:
            if mid not in self.vmemoryTable:
                print("Error: memoryScheduler._update: mid not exists")
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
            self.table[mid] = time.time()
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
        return str(self.memory), self.vmemory.getTable(), self.table, self.vmemoryTable






if __name__ == "__main__":
    pass