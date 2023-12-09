import os


class virtualMemorySim:

    def __init__(self, serverName: str):
        # location是磁盘的位置
        self.location = serverName
        os.makedirs(self.location, exist_ok=True)

        self.tablelocation = "{}/table.txt".format(self.location)
        # table是一个字典，用于存储mid和location的对应关系
        if os.path.exists(self.tablelocation):
            with open(self.tablelocation, "r+") as f:
                self.table = eval(f.read())
        else:
            self.table = {0: self.location}

    def updataTable(self):
        # 将table写入磁盘
        with open(self.tablelocation, "w+") as f:
            f.write(str(self.table))

    def read(self, mid):
        if mid not in self.table:
            return None

        templocation = self.table.get(mid)
        with open(templocation, "r") as f:
            data = f.read()
        return data

    def write(self, mid, data):

        # 将数据mid以及数据data写入磁盘
        self.table[mid] = self.location + "/{}.txt".format(mid)
        with open(self.table[mid], "w+") as f:
            f.write(data)
        self.updataTable()
        return True

    def delete(self, mid):
        if mid not in self.table:
            return False
        self.table.pop(mid)
        self.updataTable()
        return True

    def clear(self):
        self.table = {}
        self.updataTable()
        return True

    def getTable(self):
        return self.table


if __name__ == "__main__":
    diskSim = virtualMemorySim("Test")
    diskSim.clear()
    print(diskSim.getTable())
    print(diskSim.read(1))
    print(diskSim.write(1, "hello"))
    print(diskSim.read(1))
