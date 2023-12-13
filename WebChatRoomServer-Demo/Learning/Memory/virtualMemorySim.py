import os
import diskSim

class virtualMemorySim:

    def __init__(self, serverName: str, disk: diskSim):

        # disk是一个diskSim对象，虚拟内存的数据将存储在diskSim对象中
        # DiskSim = DiskSim(硬盘名称)
        # DiskSim.initialize_system_enhanced() # 初始化磁盘
        # DiskSim.write_file(文件名, 文件内容, 父目录, 文件类型) # 写入文件
        # DiskSim._mkdir(文件名, 父目录, 文件类型) # 创建目录
        # DiskSim.read_file(文件路径) # 读取文件
        # DiskSim.delete(文件路径) # 删除文件
        # DiskSim.free_space() # 返回磁盘剩余空间
        self.disk = disk
        self.serverName = serverName
        disk._mkdir("VirtualMemory", "root/"+serverName)
        self.table = {} # 虚拟内存的索引表 {"mid": "location"}
        self.location = "root/"+serverName+"/VirtualMemory"

    def read(self, mid):

        if mid not in self.table:
            return None
        file_location = self.table[mid]
        return self.disk.read_file(file_location)

    def write(self, mid, data):

        if mid in self.table:
            return False
        self.table[mid] = self.location + "/" + mid
        self.disk.write_file(mid, data, self.location, file_type="file")


    def delete(self, mid):
        if mid not in self.table:
            return False
        self.disk.delete(self.table[mid])
        self.table.pop(mid)
        return True

    def clear(self):
        self.table = {} # 虚拟内存的索引表 {"mid": "location"}
    def getTable(self):
        return self.table

