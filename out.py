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
print("|                                        更新日期：2017年8月8日|")
print("|    更新说明：                                                |")
print("|    1.增加了简单的错误检测，跳过了由于奇奇怪怪原因导致的不稳定|")
print("|     P.S.以为每个页面都那么规整的我还是太天真了               |")
print("|                                                              |")
print(" -------------------------------------------------------------- \n\n")

pku = input("\n输入pku_auth:")
a = {"pku_auth":str(pku)}
print("\nCookies确认")
print(a)
import requests
import re
import time
liveid = input("输入课程任意ID:")
print("\n正在分析课程信息\n发现课程：")
scurl = "http://www.chinesemooc.org/live/"+liveid
sc = requests.get(scurl,cookies = a)
sc.encoding = 'utf-8'
try:
    scname = re.search(r'《".*?》',sc.text)[0]
    scname = scname[4:-4]
    print(scname)
except:
    print("没有找到课程，但不一定获取失败，可以继续")
print("输出文件预处理...")
try:
    olist = []
    with open('data.csv', 'wb') as f:
        title = ["章节","标题","下载链接"]
        line = ','.join(title) + '\n'
        f.write(line.encode('UTF-8'))
except:
    print("创建数据文件失败，可能没有信息会被保存")
input("准备就绪,按回车开始")
print("\n开始处理数据，所用时间会受网络情况影响，请耐心等待\n")
url = "http://www.chinesemooc.org/live/"+liveid
r = requests.get(url,cookies = a)
r.encoding = "utf-8"
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text,"html.parser")
#print(soup.prettify())

for ul in soup.find_all("ul",attrs={"class":"round"}):
    if ul:
        for tag in ul.find_all("li"):
            try:
                print("正在处理章节" + tag.string + "\r",end ="")
                char = tag.string.replace(" ","")
                course = str(tag.attrs['data-courseid'])            
                geteidu = "http://www.chinesemooc.org/course.php?ac=course_live&op=live&course_id=" + course
                o = requests.get(geteidu,cookies = a)
                o.encoding = "utf-8"
                oorg = o.text
                oeid = re.search(r'eid.*?,',oorg)[0]
                name = re.search(r'course_name.*?,',oorg)[0]
                name = name.replace('course_name":"',"")
                name = name.replace('",',"")
                eid = re.search(r'[0-9]{5}',oeid)[0]
                furl = "http://www.chinesemooc.org/api/course_video_watch.php?course_id=" + course + "&eid=" + eid
                p = requests.get(furl,cookies = a)
                p.encoding = "utf-8"
                forg = p.text
                durl = re.search(r'http.*?\.mp4',forg)[0]
                durl = durl.replace("\\","")
                durl = durl.replace(".mp4","_HD.mp4")
                with open('data.csv', 'ab+') as f:
                    title = [char,name,durl]
                    line = ','.join(title) + '\n'
                    f.write(line.encode('UTF-8'))
            except:
                print(tag.string + "出现了一点点问题，程序继续..")
                continue
print("\n完成！感谢使用\n")
input("现在可以关闭这个程序或按回车退出")
