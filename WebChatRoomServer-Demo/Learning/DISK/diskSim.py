import time
import os
import ast


class DiskSim:

    def __init__(self, location):
        self.location = location
        if not os.path.exists(self.location):
            os.makedirs(self.location)
            self.initialize_system_enhanced()
            self.freeSpace = 1024
        else:
            with open(self.location + "\\Boot.txt", "r") as boot:
                self.freeSpace = int(boot.read())

    def initialize_system_enhanced(self):
        # 初始化 Table, Disk, catalog 文件
        with open(self.location + "\\Table.txt", "w") as table, open(self.location + "\\Disk.txt", "w") as disk, open(
                self.location + "\\catalog.txt", "w") as catalog, open(self.location + "\\Boot.txt", "w") as boot:
            # 初始化 Boot， 用于记录磁盘的状态
            boot.write("1024")

            # 初始化 Table 文件内容，每个块占一行。开始行为当前disk状态，包括空闲块和已用块数量。
            table.write("__EMPTY__\n" * 1024)  # 假设有 1024 个块

            # 初始化 Disk 文件内容
            disk.write((" " * 1024 + "__\n") * 1024)  # 假设每个块有 1028位，前1024位作为数据存储，后两位作为下一个区块的索引以及换行符\n。

            # 初始化 catalog 文件内容
            catalog.write(
                "[Identifier,Name,Type,Parent (1 root),Children [1,2,3],StartBlock,Size]\n"
                "[0000, 'root', 'dir', 0, [], 0, 0]")  # 文件名，标识符，类型，父目录(目录行号)，开始块号([目录行号])，大小

    def free_space(self):
        # 读取Table文件，返回空闲块的数量
        with open(self.location + "Table.txt", "r") as table:
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
        with open(self.location + "\\catalog.txt", "r") as catalog:
            lines = catalog.readlines()
        # 从根目录开始寻找目标文件夹
        for i in range(len(targetLoc) - 1):
            if i == 0:
                children = eval(lines[1])[4]
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

    def create_dir(self, name, parent="root", file_type="dir"):
        # 生成一个独特的标识符
        unique_id = f"{name}_{int(time.time())}"

        with open(self.location + "\\catalog.txt", "a+") as catalog:
            catalog.seek(0)
            lines = catalog.readlines()

            parent_num = self.get_line_of_parent(parent)
            if parent_num is False:
                print("!!!parent not found")
                return False

            # Convert the string from the file into a list object
            parentCatalog = ast.literal_eval(lines[parent_num].strip())
            parentCatalog[4].append(len(lines))

            # Convert back to string and update the line
            lines[parent_num] = str(parentCatalog) + "\n"

            # Prepare new entry as a string
            new_entry = str([unique_id, name, file_type, parent_num, [], 9999, 0]) + "\n"

            lines.append(new_entry)

            # Write updated lines back to catalog
            catalog.seek(0)
            catalog.truncate()
            catalog.writelines(lines)
        return True

    def write_file_with_identifier(self, name, data, parent="root", file_type="file"):
        # 生成一个独特的标识符
        unique_id = f"{name}_{int(time.time())}"

        with open(self.location + "\\Table.txt", "r") as table:
            blocks = table.readlines()

        start_blocks = []
        w2b = []
        free_blocks = 0
        required_blocks = len(data) // 1024 + (1 if len(data) % 1024 > 0 else 0)

        if required_blocks > self.freeSpace:
            return False

        # 寻找连续的空闲块
        for i, block in enumerate(blocks):
            if block.strip() == "__EMPTY__":
                free_blocks += 1
                w2b.append(i)
                required_blocks -= 1
                if required_blocks == 0:
                    break

        print(w2b, "w2b")

        with open(self.location + "\\catalog.txt", "a+") as catalog:
            catalog.seek(0)
            lines = catalog.readlines()

            parent_num = self.get_line_of_parent(parent)
            if parent_num is False:
                print("!!!parent not found")
                return False

            # Convert the string from the file into a list object
            parentCatalog = ast.literal_eval(lines[parent_num].strip())
            parentCatalog[4].append(len(lines))

            # Convert back to string and update the line
            lines[parent_num] = str(parentCatalog) + "\n"

            # Prepare new entry as a string
            first_block = w2b[0] if len(w2b) > 0 else 0
            new_entry = str([unique_id, name, file_type, parent_num, [], first_block, len(data)]) + "\n"

            lines.append(new_entry)

            # Write updated lines back to catalog
            with open(self.location + "\\Table.txt", "w+") as table, open(self.location + "\\Disk.txt", "r+") as disk:
                # 更新 Table 和 Disk 文件
                for i in range(len(w2b)):
                    start_blocks = w2b[i]
                    blocks[start_blocks] = f"Used by {unique_id}\n"
                    self.freeSpace -= 1
                    disk.seek(start_blocks * 1028)  # 定位到开始块
                    if i + 1 == len(w2b):
                        disk.write(data[i * 1024:])
                    else:
                        disk.write(data[i * 1024:(i + 1) * 1024] + "{:2x}\n".format(
                            w2b[i + 1] - w2b[i]))  # 写入数据 + 下一块的索引(十六进制偏移量)
                table.writelines(blocks)

            catalog.seek(0)
            catalog.truncate()
            catalog.writelines(lines)
        with open(self.location + "\\Boot.txt", "w") as boot:
            boot.write(str(self.freeSpace))

        return True

    def delete_file(self, path):

        parent_path, name = os.path.split(path)

        # Get the parent directory's line number
        parent_num = self.get_line_of_parent(parent_path)
        if parent_num is False:
            print("Parent directory not found")
            return False

        # Locate the file in the catalog
        with open(self.location + "\\catalog.txt", "r") as catalog:
            lines = catalog.readlines()

        file_line_num = None
        for line in lines:
            entry = ast.literal_eval(line.strip())
            if entry[1] == name and entry[3] == parent_num:
                file_line_num = lines.index(line)
                start_block = entry[5]
                size = entry[6]
                break
        else:
            print("File not found")
            return False

        # Remove the file entry from the catalog and update the parent directory
        with open(self.location + "\\catalog.txt", "r+") as catalog:
            parent_entry = ast.literal_eval(lines[parent_num].strip())
            parent_entry[4].remove(file_line_num)
            lines[parent_num] = str(parent_entry) + "\n"

            catalog.seek(0)
            catalog.truncate()
            for i, line in enumerate(lines):
                if i != file_line_num:
                    catalog.write(line)

        # Update the Table and Disk
        with open(self.location + "\\Table.txt", "r+") as table, open(self.location + "\\Disk.txt", "r+") as disk:
            blocks = table.readlines()
            table.seek(0)
            table.truncate()
            remaining_size = size
            current_block = start_block
            while remaining_size > 0:
                blocks[current_block] = "__EMPTY__\n"
                self.freeSpace += 1
                disk.seek(current_block * 1028)
                disk_data = disk.read(1024)
                remaining_size -= len(disk_data)
                if remaining_size > 0:
                    current_block = int(disk.read(2), 16)
            table.writelines(blocks)

        # Update the Boot file
        with open(self.location + "\\Boot.txt", "w") as boot:
            boot.write(str(self.freeSpace))

        return True


diskSim = DiskSim("Test")
diskSim.initialize_system_enhanced()
diskSim.write_file_with_identifier("test", "test", "root/test", "file")
diskSim.create_dir("test", "root", "dir")
diskSim.write_file_with_identifier("test", "test", "root/test", "file")
diskSim.create_dir("largefolder", "root", "dir")
diskSim.create_dir("largefolder2", "root/largefolder", "dir")
diskSim.write_file_with_identifier("test", 'A' * 3000, "root/largefolder/largefolder2", "file")
