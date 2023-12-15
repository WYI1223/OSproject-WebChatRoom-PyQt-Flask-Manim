import diskSim


# 简易文件读取系统

while(True):
    diskSim = diskSim.diskSim(input("Please input the disk name: "))
    pwd = "root"
    while(True):
        print("Please input the command:")
        print("1. cd")
        print("2. ls")
        print("3. read")
        print("4. Exit")
        command = input()
        if(command == "1"):
            pwd = pwd +"/"+ input("Please input the path: ")
        elif(command == "2"):
            print("pwd: " + pwd)
            print(diskSim._ls(pwd))
        elif(command == "3"):
            print("pwd: " + pwd)
            print(diskSim.read_file(pwd + input("Please input the file name: ")))
        elif(command == "4"):
            break
        else:
            print("Invalid command!")