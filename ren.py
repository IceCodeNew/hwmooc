print(" ----------------------文件批量重命名工具---------------------- ")
print("|                 By：tdh0602 From：吾爱破解论坛               |")
print("|                                                              |")
print("|    *data.csv和视频文件应与本程序出于相同目录下               |")
print("|    使用说明：                                                |")
print("|    1.data.csv为数据文件，编码格式应为UTF-8                   |")
print("|    2.所下载的视频名称应与链接名称一致                        |")
print("|                                                              |")
print("|                                                              |")
print("|                                        更新日期：2017年8月9日|")
print("|                                                              |")
print(" -------------------------------------------------------------- \n\n")

import csv
import os
import re

csv_reader = csv.reader(open('data.csv', encoding='utf-8'))
lesson = input("请输入课程名以开始：\n")
i = -1
for row in csv_reader:
    i = i + 1
    try:
        old = re.search(r'/\d+-\d+\.mp4', row[1])[0][1:]
        new = lesson + "-" + row[0] + ".mp4"
        print("尝试把 " + old + " 重命名为 " + new)
        os.rename(old, new)
    except:
        continue

input("处理完成，按回车键结束程序")
