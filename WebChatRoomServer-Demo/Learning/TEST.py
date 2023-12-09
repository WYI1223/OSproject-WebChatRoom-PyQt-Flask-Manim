import time

def initialize_system_enhanced():
    # 初始化 Table, Disk, catalog 文件
    with open("Table.txt", "w") as table, open("Disk.txt", "w") as disk, open("catalog.txt", "w") as catalog:
        # 初始化 Table 文件内容
        table.write("__EMPTY__\n" * 1024)  # 假设有 1024 个块

        # 初始化 Disk 文件内容
        disk.write(" " * 1024 * 1024)  # 假设每个块有 1KB，总共 1MB 的空间

        # 初始化 catalog 文件内容
        catalog.write("Name,Identifier,Type,Parent,StartBlock,Size\n")  # 文件名，标识符，类型，父目录，开始块号，大小


def write_file_with_identifier(name, data, parent="root", file_type="file"):
    # 生成一个独特的标识符
    unique_id = f"{name}_{int(time.time())}"

    try:
        with open("Table.txt", "r") as table:
            blocks = table.readlines()
    except FileNotFoundError:
        with open("Table.txt", "w+") as table:
            blocks = table.readlines()


    # 寻找连续的空闲块
    start_blocks = []
    free_blocks = 0
    required_blocks = len(data) // 1024 + (1 if len(data) % 1024 > 0 else 0)

    for i, block in enumerate(blocks):
        if block.strip() == "__EMPTY__":
            if free_blocks == 0:
                start_blocks.append(i)
            free_blocks += 1
            if free_blocks >= required_blocks:
                break
        else:
            free_blocks = 0

    if free_blocks >= required_blocks:
        # 更新 Table 和 Disk 文件
        with open("Table.txt", "w") as table, open("Disk.txt", "r+") as disk:
            current_block = 0
            for start_block in start_blocks:
                for i in range(start_block, start_block + free_blocks):
                    blocks[i] = f"Used by {unique_id}\n"
                    if current_block * 1024 < len(data):
                        disk.seek(i * 1024)  # 定位到开始块
                        disk.write(data[current_block * 1024:(current_block + 1) * 1024])  # 写入数据
                        current_block += 1
            table.writelines(blocks)

        # 更新 catalog 文件
        with open("catalog.txt", "a") as catalog:
            catalog.write(f"{name},{unique_id},{file_type},{parent},{start_blocks[0]},{len(data)}\n")

    else:
        print("Not enough space!")


initialize_system_enhanced()
write_file_with_identifier("myFolder", "", "root", "dir")
write_file_with_identifier("myFile", "a" * 1024, "myFolder", "file")

