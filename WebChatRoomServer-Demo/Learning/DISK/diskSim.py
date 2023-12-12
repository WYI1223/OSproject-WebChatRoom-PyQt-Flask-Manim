import os
import ast

# DiskSim = DiskSim(硬盘名称)
# DiskSim.initialize_system_enhanced() # 初始化磁盘
# DiskSim.write_file_with_identifier(文件名, 文件内容, 父目录, 文件类型) # 写入文件
# DiskSim.create_dir(文件名, 父目录, 文件类型) # 创建目录
# DiskSim.read_file(文件路径) # 读取文件
# DiskSim.delete(文件路径) # 删除文件
# DiskSim.free_space() # 返回磁盘剩余空间


class diskSim:


    def __init__(self, location):
        self.location = location
        self.unique_id = 1
        self.diskLoc = self.location + "\\Disk"
        self.catalogLoc = self.location + "\\catalog"
        self.tableLoc = self.location + "\\Table"
        self.bootLoc = self.location + "\\Boot"
        if not os.path.exists(self.location):
            os.makedirs(self.location)
            self.initialize_system_enhanced()
            self.freeSpace = 1024
        else:
            with open(self.location + "\\Boot", "r") as boot:
                self.freeSpace = int(boot.read())


    def initialize_system_enhanced(self):
        # 初始化 Table, Disk, catalog 文件
        with open(self.tableLoc, "w+") as table, open(self.diskLoc, "w+") as disk, open(
                self.catalogLoc, "w+") as catalog, open(self.bootLoc, "w+") as boot:
            # 初始化 Boot， 用于记录磁盘的状态
            boot.write("1024")
            self.freeSpace = 1024

            # 初始化 Table 文件内容，每个块占一行。开始行为当前disk状态，包括空闲块和已用块数量。
            table.write("__EMPTY__\n" * 1024)  # 假设有 1024 个块

            # 初始化 Disk 文件内容
            disk.write((" " * 1024 + "__\n") * 1024)  # 假设每个块有 1028位，前1024位作为数据存储，后两位作为下一个区块的索引以及换行符\n。

            # 初始化 catalog 文件内容
            catalog.write(
                "[Identifier,Name,Type,Parent (1 root),Children [1,2,3],StartBlock,Size]\n"
                "[0000, 'root', 'dir', 0, [], 0, 0]\n"
                +"\n"*1024)  # 文件名，标识符，类型，父目录(目录行号)，开始块号([目录行号])，大小

    def free_space(self):
        # 读取Table文件，返回空闲块的数量
        with open(self.tableLoc, "r") as table:
            blocks = table.readlines()
        free_blocks = 0
        for i, block in enumerate(blocks):
            if block.strip() == "__EMPTY__":
                free_blocks += 1
        return free_blocks

    def get_line_of_parent(self, parent):
        targetLoc = parent.split("/")
        if targetLoc[0] == "root":
            targetLoc[0] = 1
        with open(self.catalogLoc, "r") as catalog:
            lines = catalog.readlines()
        # 从根目录开始寻找目标文件夹
        for i in range(len(targetLoc) - 1):
            if i == 0:
                children = eval(lines[1])[4]
            if children == [False]:
                return False
            if len(children) == 0:
                return False
            else:
                # 当前目录下有子目录，遍历子目录名字，找到目标文件夹
                for child in children:

                    currentName = eval(lines[child])[1]

                    # 如果当前目录名字和目标文件夹名字相同，进入下一层目录
                    if currentName == targetLoc[i + 1]:
                        targetLoc[i + 1] = child
                        children = eval(lines[child])[4]
                        break
                    else:
                        continue

        return targetLoc[-1]

    def find_first_empty_table(self):
        with open(self.catalogLoc, "r") as catalog:
            lines = catalog.readlines()
        for i, block in enumerate(lines):
            if i <= 1:
                continue
            if block == '\n':
                return i
        return False

    def replace_line_by_index(self, file_path, index, newcontent=""):
        # Step 1: Read the file and load its content into a list
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Ensure the index is within the range of the file's lines
        if 0 <= index < len(lines):
            # Step 2: Remove the specified line
            lines[index] = newcontent
            # Step 3: Write the updated list back to the file
            with open(file_path, 'w') as file:
                file.writelines(lines)
        else:
            print(f"Index {index} is out of range for the file.")

    def create_dir(self, name, parent="root", file_type="dir"):
        # 生成一个独特的标识符


        with open(self.catalogLoc, "r") as catalog:
            catalog.seek(0)
            lines = catalog.readlines()

            parent_num = self.get_line_of_parent(parent)
            if parent_num is False:
                print("!!!parent not found")
                return False

            inerset_line = self.find_first_empty_table()
            # Convert the string from the file into a list object
            parentCatalog = ast.literal_eval(lines[parent_num].strip())
            parentCatalog[4].append(inerset_line)

            # Convert back to string and update the line
            self.replace_line_by_index(self.catalogLoc, parent_num, str(parentCatalog) + "\n")

            # Prepare new entry as a string
            new_entry = str([self.unique_id , name, file_type, parent_num, [], 9999, 0]) + "\n"
            self.unique_id += 1
            self.replace_line_by_index(self.catalogLoc, inerset_line, new_entry)

            # Write updated lines back to catalog
            # catalog.seek(0)
            # catalog.truncate()
            # catalog.writelines(lines)
        return True

    def write_file_with_identifier(self, name, data, parent="root", file_type="file"):
        # 生成一个独特的标识符

        with open(self.tableLoc, "r") as table:
            blocks = table.readlines()

        insert_line = self.find_first_empty_table()

        w2b = []
        free_blocks = 0
        required_blocks = len(data) // 1024 + (1 if len(data) % 1024 > 0 else 0)

        if required_blocks > self.freeSpace:
            return False

        # 寻找空闲块
        for i, block in enumerate(blocks):
            if block.strip() == "__EMPTY__":
                free_blocks += 1
                w2b.append(i)
                required_blocks -= 1
                if required_blocks == 0:
                    break

        # print(w2b, "w2b")

        with open(self.catalogLoc, "r") as catalog:
            catalog.seek(0)
            lines = catalog.readlines()

            parent_num = self.get_line_of_parent(parent)
            if parent_num is False:
                print("!!!parent not found")
                return False

            # Convert the string from the file into a list object
            parentCatalog = ast.literal_eval(lines[parent_num].strip())
            parentCatalog[4].append(insert_line)

            # Convert back to string and update the line
            self.replace_line_by_index(self.catalogLoc, parent_num, str(parentCatalog) + "\n")


            # Prepare new entry as a string
            first_block = w2b[0] if len(w2b) > 0 else 0
            new_entry = str([self.unique_id, name, file_type, parent_num, [], first_block, len(data)]) + "\n"
            self.unique_id += 1
            self.replace_line_by_index(self.catalogLoc, insert_line, new_entry)

            # Write updated lines back to catalog
            with open(self.tableLoc, "w+") as table, open(self.diskLoc, "r+") as disk:
                # 更新 Table 和 Disk 文件
                for i in range(len(w2b)):
                    start_blocks = w2b[i]
                    blocks[start_blocks] = f"{self.unique_id}\n"
                    disk.seek(start_blocks * 1028)  # 定位到开始块
                    if i + 1 == len(w2b):
                        disk.write(data[i * 1024:])
                        self.freeSpace -= 1
                    else:
                        disk.write(data[i * 1024:(i + 1) * 1024] + "{:2x}\n".format(
                            w2b[i + 1] - w2b[i]))  # 写入数据 + 下一块的索引(十六进制偏移量)
                        self.freeSpace -= 1
                table.writelines(blocks)

            # catalog.seek(0)
            # catalog.truncate()
            # catalog.writelines(lines)
        with open(self.bootLoc, "w") as boot:
            boot.write(str(self.freeSpace))

        return True

    def read_file(self, path:str):
        target = self.get_line_of_parent(path)
        if target is False:
            return False
        with open(self.catalogLoc, "r") as catalog:
            lines = catalog.readlines()
            AimCatalog = eval(lines[target])
        if AimCatalog[2] == "dir":
            # 返回目录下的文件名
            # [Identifier,Name,Type,Parent (1 root),Children [1,2,3],StartBlock,Size]
            return AimCatalog[4]
        else:

            # 返回文件内容
            # 如果文件大小为0，返回空字符串
            if AimCatalog[6] == 0:
                return ""
            with open(self.diskLoc, "r") as disk:
                # 定位到文件开始块
                disk.seek(AimCatalog[5] * 1028)
                # 如果文件大小小于1024，直接读取
                if AimCatalog[6] < 1024:
                    return disk.read(AimCatalog[6])
                # 如果文件大小大于1024，需要读取多个块
                else:
                    block_num = AimCatalog[6] // 1024 + (1 if AimCatalog[6] % 1024 > 0 else 0)
                    data = ""
                    for i in range(block_num):
                        data += disk.read(1024)
                        disk.seek(int(disk.read(2), 16) * 1028)
                    return data



    def delete(self, path):
        target_line = self.get_line_of_parent(path)
        if target_line is False:
            print("!!!target not found")
            return False

        with open(self.catalogLoc, "r") as catalog:
            lines = catalog.readlines()

        target_entry = eval(lines[target_line])

        # If the target is a directory, recursively delete its contents
        if target_entry[2] == "dir":
            for child in target_entry[4]:
                child_path = path + "/" + eval(lines[child])[1]
                self.delete(child_path)


        # Remove the target entry from the catalog
        self.replace_line_by_index(self.catalogLoc, target_line, "\n")

        # Update parent directory's children list
        parent_line = target_entry[3]
        if parent_line != 1:  # not root
            parent_entry = eval(lines[parent_line].strip())
            parent_entry[4].remove(target_line)
            self.replace_line_by_index(self.catalogLoc, parent_line, str(parent_entry) + "\n")

        # Free up the blocks used by the file or the directory
        if target_entry[2] == "file":
            self.free_blocks(target_entry[5], target_entry[6])

    def free_blocks(self, start_block, size):
        # 释放文件占用的块
        block_num = size // 1024 + (1 if size % 1024 > 0 else 0)
        current_block = start_block
        reamining_blocks = block_num

        for _ in range(block_num):
            self.replace_line_by_index(self.tableLoc, current_block, "__EMPTY__\n")
            with open(self.diskLoc, "r+") as disk:
                disk.seek(current_block * 1028)
                # 当目前数据块为最后一个块时，直接清空
                if reamining_blocks == 1:
                    self.replace_line_by_index(self.diskLoc, current_block, " " * 1024 + "__\n")
                    break
                data = disk.read(1026)  # Read block data and next block index
                next_block_str = data[-2:] # Get next block index
                current_block = current_block + int(next_block_str, 16)
                reamining_blocks -= 1
                self.freeSpace += 1
        with open(self.bootLoc, "w") as boot:
            boot.write(str(self.freeSpace))



diskSim = diskSim("Test")
diskSim.initialize_system_enhanced()
diskSim.write_file_with_identifier("test", "test", "root/test", "file")
diskSim.create_dir("test", "root", "dir")
diskSim.write_file_with_identifier("test", "test", "root/test", "file")
diskSim.create_dir("largefolder", "root", "dir")
diskSim.create_dir("largefolder2", "root/largefolder", "dir")
diskSim.write_file_with_identifier("test", 'A' * 3000, "root/largefolder/largefolder2", "file")
diskSim.write_file_with_identifier("test", 'A' * 3000, "root/largefolder", "file")
diskSim.create_dir("largefolder1", "root", "dir")
diskSim.delete("root/largefolder")
diskSim.write_file_with_identifier("test1", "test1", "root/test", "file")
diskSim.create_dir("test", "root", "dir")
diskSim.write_file_with_identifier("test2", "test2", "root/test", "file")
diskSim.create_dir("largefolder", "root", "dir")
diskSim.create_dir("largefolder2", "root/largefolder", "dir")
diskSim.write_file_with_identifier("test", 'A' * 3000, "root/largefolder/largefolder2", "file")
diskSim.write_file_with_identifier("test", 'A' * 3000, "root/largefolder", "file")
diskSim.create_dir("largefolder1", "root", "dir")
diskSim.delete("root/largefolder")
print(diskSim.read_file("root/test"))
print(diskSim.read_file("root/test1"))
print(diskSim.read_file("root/test/test2"))
print(diskSim.read_file("root/largefolder1"))