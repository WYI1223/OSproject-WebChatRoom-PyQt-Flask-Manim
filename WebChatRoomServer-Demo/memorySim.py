class memorySim:

    def __init__(self, length):

        self.table = {}
        self.blockstatus = [False] * length
        self.block = {i: None for i in range(length)}
        self.size = 0
    def add(self, mid, data):
        length = len(self.blockstatus)
        if mid in self.table:
            self.delete(mid)

        if self.size+1 > length:
            return False
        for i in range(length):
            if not self.blockstatus[i]:
                self.blockstatus[i] = True
                self.block[i] = data
                self.table[mid] = i
                self.size += 1
                return True

    def get(self, mid):
        if mid not in self.table:
            return None
        index = self.table[mid]
        return self.block[index]

    def delete(self, mid):
        if mid not in self.table:
            raise KeyError("No such memory mid:", mid)
        index = self.table[mid]
        self.blockstatus[index] = False
        self.block[index] = None
        self.table.pop(mid)
        self.size -= 1
        return True

    def clear(self):
        self.table = {}
        self.blockstatus = [False] * len(self.blockstatus)
        self.block = {i: None for i in self.block}
        self.size = 0
        return True

    def __str__(self):
        return str(self.table), str(self.blockstatus), str(self.block), str(self.size)

    def getMemory(self):
        return ((v,k) for k,v in self.table.items())


