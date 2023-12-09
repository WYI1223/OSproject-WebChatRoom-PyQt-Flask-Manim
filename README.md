# OSproject-WebChatRoom-PyQt-Flask-Manim
 OSproject-WebChatRoom-PyQt-Flask-Manim

## Learning Line
- [ ] PyQt5
- https://www.bilibili.com/video/BV12B4y1h7QX/?spm_id_from=333.788.recommend_more_video.0&vd_source=2755821873fe338531f662ab376e426b
- https://www.bilibili.com/video/BV14g411h7cQ/?spm_id_from=autoNext&vd_source=2755821873fe338531f662ab376e426b
- [ ] Flask
- https://chat.openai.com/share/0819f6a2-3601-4a1a-831f-2028db982e8d
- [ ] Manim
- https://chat.openai.com/share/afb47da5-b8f5-4f92-b136-71307050a7d9
- [ ] Memory Sim
- [ ] File System Sim - FAT
  - [x] Feature
    - [x] Limited Space
    - [x] Less search operation
    - [x] Offline availble
  - [ ] Function
    - [x] Write
    - [x] Dir
    - [x] read
    - [ ] move
- [ ] thread system Sim




### 参考内容


1. CSS cheatsheet: https://htmlcheatsheet.com/css/
2. 【Python 实现操作系统模型 [南京大学2023操作系统-P4] (蒋炎岩)】  https://www.bilibili.com/video/BV1Zb411D7jE/?share_source=copy_web&vd_source=da0575add73694307a909c8c9c1845e9&t=4040
3. FAT
    1. Operation System Concepts chap13 - 14: https://os-book.com/OS10/slide-dir/index.html
    2. An Overview of FAT12: https://oriont.net/posts/fat12-overview
    3. Design of the FAT file system, wikipedia: https://en.wikipedia.org/wiki/Design_of_the_FAT_file_system
4. 

#### 在项目中得到的一些启发
1. FAT
   1. 读取文件时
   2. 删除文件时
       1. 当删除catalog中目标行时，有两种方案可以选择
           1. 替换当前行为/n (本项目选择此处理方法)
              1. 优点：不需要移动后面的行，在删除时效率高
              2. 缺点：需要在读取时判断当前行是否为/n，如果是则跳过，增大了读取时的复杂度
           2. 删除当前行，让后面的行前移
              1. 优点：创建新文件时不需要判断当前行是否为/n，减小了创建时的复杂度，不需要在每次创建时都要遍历整个catalog直到第一个/n
              2. 缺点：删除时需要移动后面的行，效率较低，并且在删除时，需要考虑其他行中是否有删除行后的索引，如果有则需要全部更新
                 - 还有一点不确定的是，如果移动后面的行，是否也增加了更多的操作