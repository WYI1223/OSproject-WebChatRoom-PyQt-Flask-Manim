from Memory import diskSim

class recordChat():
    def __init__(self, disk:diskSim, serverName):
        self.disk = disk
        self.serverName = serverName
        self.disk._mkdir("record", "root/"+serverName)
        self.recordloc = "root/"+serverName+"/record"
        self.num = self.disk.read_file(self.recordloc+"/num")
        if self.num == False:
            self.num = 0
            self.disk.wrtie_file("num",0,self.recordloc)
        else:
            self.num = int(self.num)

    def put(self, record):
        # DiskSim.write_file(文件名, 文件内容, 父目录, 文件类型) # 写入文件
        self.num += 1
        self.disk.wrtie_file(str(self.num), record, self.recordloc)
        self.disk.wrtie_file("num",self.num,self.recordloc)

    def get(self):
        record_list = self.disk._ls(self.recordloc)
        record = []
        for i in record_list:
            record.append(self.disk.read_file(self.recordloc+"/"+i))
        return record