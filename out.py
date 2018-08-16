print(" -----------------------华文慕课视频下载----------------------- ")
print("|                 By:tdh0602 From:吾爱破解                     |")
print("|              访问www.52pojie.cn获取更多资源                  |")
print("|                                                              |")
print("|                                                              |")
print("|    使用说明：                                                |")
print("|    1.需要输入Cookies中的pku_auth的内容，请使用浏览器工具查看 |")
print("|    2.课程ID为该门课程播放页面URL中的ID信息，具体查看论坛发布 |")
print("|      帖中的相关说明。                                        |")
print("|    3.获取的下载链接默认为HD（高清）格式，若课程无高清品质，请|")
print("|      自行替换链接中_HD部分为_LD/_SD/无 来实现其他品质视频下载|")
print("|    4.获取到的全部信息以UTF-8编码形式存储于当前目录下data.csv |")
print("|      文件中，直接使用Excel打开可能产生乱码，请先转码ANSI     |")
print("|                                                              |")
print("|                                                              |")
print("|                                        更新日期：2017年8月9日|")
print("|    更新说明：                                                |")
print("|    1.设定超时时间为15秒，避免部分视频无法解析导致的长时间停滞|")
print("|    2.优化错误提示                                            |")
print("|    3.对获取视频下载地址增加可选的延时                        |")
print("|    4.使用IE10的User-agent进行访问                            |")
print("|                                                              |")
print(" -------------------------------------------------------------- \n\n")
kv = {"user-agent": "Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)"}
pku = input("\n输入pku_auth:")
a = {"pku_auth": str(pku)}
print("\nCookies确认")
print(a)
import re
import time

import requests

liveid = input("输入课程任意ID:")
print("\n正在分析课程信息")
scurl = "http://www.chinesemooc.org/live/" + liveid
try:
    sc = requests.get(scurl, cookies=a, timeout=15, headers=kv)
    sc.raise_for_status()
    sc.encoding = 'utf-8'
except:
    print("Error：网络连接超时")

try:
    scname = re.search(r'《".*?》', sc.text)[0]
    scname = scname[4:-4]
    print("\n发现课程：")
    print(scname)
except:
    print("没有找到课程，但不一定获取失败，可以继续")
print("输出文件预处理...")
try:
    olist = []
    with open('data.csv', 'wb') as f:
        title = ["章节", "下载链接"]
        line = ','.join(title) + '\n'
        f.write(line.encode('UTF-8'))
except:
    print("创建数据文件失败，可能没有信息会被保存")

de = input("\n准备就绪\n为避免服务器拒绝访问，每个视频下载链接获取成功后可选3秒延时\n输入大写字母N按回车来启用延时，否则请直接按回车开始")
print("\n开始处理数据,请耐心等待\n")
url = "http://www.chinesemooc.org/live/" + liveid
r = requests.get(url, cookies=a, timeout=15, headers=kv)
r.encoding = "utf-8"
from bs4 import BeautifulSoup

soup = BeautifulSoup(r.text, "html.parser")

for ul in soup.find_all("ul", attrs={"class": "round"}):
    if ul:
        for tag in ul.find_all("li"):
            try:
                course = str(tag.attrs['data-courseid'])
                geteidu = "http://www.chinesemooc.org/course.php?ac=course_live&op=live&course_id=" + course
                obj = requests.get(geteidu, cookies=a, timeout=15, headers=kv)
                obj.encoding = "utf-8"
                obj_content = obj.text
                obj_eid_list = re.findall(r'eid.*?\d\"', obj_content)

                for index in range(len(obj_eid_list)):
                    char = tag.string.replace(" ", "") + "." + str(index + 1)
                    print("正在处理章节" + char + "\n", end="")

                    eid = re.search(r'\d{5}', obj_eid_list[index]).string
                    eid = eid.replace("eid\":\"", "")
                    eid = eid.replace("\"", "")
                    furl = "http://www.chinesemooc.org/api/course_video_watch.php?course_id=" + course + "&eid=" + eid
                    page = requests.get(furl, cookies=a, timeout=15, headers=kv)
                    page.encoding = "utf-8"
                    page_content = page.text
                    obj_url = re.search(r'mp4_url.*?mp4\"', page_content)
                    durl = obj_url[0].replace("mp4_url\":\"", "")
                    durl = durl.replace("\\", "")
                    durl = durl.replace("\"", "")
                    with open('data.csv', 'ab+') as f:
                        title = [char, durl]
                        line = ','.join(title) + '\n'
                        f.write(line.encode('UTF-8'))
                    if de != 'N':
                        sleep_second = 3
                        print("延时等待 " + str(sleep_second) + " 秒…\n", end="")
                        time.sleep(sleep_second)
            except:
                print("在获取章节 " + char + " 过程中出现了些问题，可能是网络连接超时或本章节无视频，错误将被忽略并继续")
                continue
print("\n完成！感谢使用\n")
input("现在可以关闭这个程序或按回车退出")
