class memorySim:

    def __init__(self, length):

        self.memory = []
        self.placeholder = []
        self.lengthLimit = length

    def add(self, index, data):
        if index > self.lengthLimit:
            return False
        self.placeholder[index] = True
        self.memory[index] = data
        return True

    def get(self, index):
        if index > self.lengthLimit:
            return None
        return self.memory[index]

    def delete(self, index):
        if index > self.lengthLimit:
            return False
        self.placeholder[index] = False
        return True

    def clear(self):
        self.memory = []
        self.placeholder = []

    def getMemory(self):
        return self.placeholder, self.memory



