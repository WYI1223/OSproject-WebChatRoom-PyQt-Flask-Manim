import time

from Memory import diskSim

class logSystem:

    def __init__(self, disk:diskSim, serverName):

        self.disk = disk
        self.serverName = serverName
        self.disk._mkdir("log", "root/"+serverName)
        self.logloc = "root/"+serverName+"/log"
        self.num = self.disk.read_file(self.logloc+"/num")
        if self.num == False:
            self.num = 0
            self.disk.wrtie_file("num",0,self.logloc)
        else:
            self.num = int(self.num)


    def put(self, log):
        # DiskSim.write_file(文件名, 文件内容, 父目录, 文件类型) # 写入文件
        self.num += 1
        self.disk.wrtie_file(time.get_clock_info(), log, self.logloc)
        self.disk.wrtie_file("num",self.num,self.logloc)

    def get(self):
        log_list = self.disk._ls(self.logloc)
        log = []
        for i in log_list:
            log.append(self.disk.read_file(self.logloc+"/"+i))
        return log

    def clear(self):
        self.disk.delete(self.logloc)
        self.disk._mkdir("log", "root/"+self.serverName)
        self.logloc = "root/"+self.serverName+"/log"
        self.num = self.disk.read_file(self.logloc+"/num")
        if self.num == False:
            self.num = 0
            self.disk.wrtie_file("num",0,self.logloc)
        else:
            self.num = int(self.num)