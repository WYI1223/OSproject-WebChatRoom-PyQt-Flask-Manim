class memorySim:

    def __init__(self, length):

        self.table = [False] * length
        self.cata = {}
        self.counter = {}
        self.memSpace = length

    def add(self, mid, data):

        # 先判断是否有空间
        if self.memSpace == 0:
            return False

        # 如果有空间，判断是否已经存在
        if mid in self.table:
            return False

        # 如果不存在，加入到内存中
        for i in range(len(self.table)):
            if not self.table[i]:
                self.table[i] = True
                self.cata[mid] = i
                self.counter[mid] = data
                self.memSpace -= 1
                return True
        print("Error: memorySim.add: memSpace != 0, but no space")

    def get(self, mid):

        if mid not in self.cata:
            return False
        else:
            return self.counter[mid]

    def delete(self, mid):

        if mid not in self.cata:
            return False
        else:
            self.table[self.cata[mid]] = False
            self.counter.pop(mid)
            self.cata.pop(mid)
            self.memSpace += 1
            return True

    def change(self, mid, data):
        if mid not in self.cata:
            return False
        else:
            self.counter[mid] = data
            return True

    def clear(self):
        self.table = [False] * len(self.table)
        self.cata = {}
        self.counter = {}
        self.memSpace = len(self.table)

    def __str__(self):
        memory_status = "Memory Status:\n"

        for i, is_used in enumerate(self.table):
            memory_status += f"  Block {i + 1}: {'Used' if is_used else 'Free'}\n"

        memory_status += "\nCatalog:\n"
        for mid, index in self.cata.items():
            memory_status += f"  {mid} -> Block {index + 1}\n"

        memory_status += "\nCounter:\n"
        for mid, data in self.counter.items():
            memory_status += f"  {mid} -> {data}\n"

        memory_status += f"\nFree Space: {self.memSpace} blocks\n"

        return memory_status


