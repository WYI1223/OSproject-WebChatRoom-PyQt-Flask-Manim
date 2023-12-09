import memorySim
import virtualMemorySim

class memoryScheduler:

    def __init__(self, serverName, length):
        self.table = {}
        self.memorySim = memorySim.memorySim(length)
        self.virtualMemorySim =virtualMemorySim.virtualMemorySim(serverName)


if __name__ == "__main__":
    pass