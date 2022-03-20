import requests
from lxml import etree
import os
import time,random

def GetOneBook(url):
    directory=requests.get(url,headers=headers).text
    bookname_list=etree.HTML(directory).xpath('/html/body/div[1]/div[3]/div[2]/h1/text()')
    if 0 ==len(bookname_list):# 确认小说正常存在
        return
    
    # 1. 创建书文件夹
    bookname=bookname_list[0]
    path=NewFolder(url.split('/')[-3]+"_"+bookname)# print(url.split('/'))

    volume_list=etree.HTML(directory).xpath('/html/body/div[1]/div[3]/div[@class="story-catalog"]')
    # 2. 每卷操作
    for volume in volume_list:
        print(volume_list[0])
        print(volume)
        if volume==volume_list[0]:
            continue
        volumename=volume.xpath('./div[@class="catalog-hd"]/h3/text()')[0]
        print(volumename)
        with open(path+volumename+".md","a",encoding='utf-8') as file:# 解决编码问题(有些文章中有Unicode表情) 解决方案链接 : https://www.cnblogs.com/themost/p/6603409.html
            
            chapter_list=volume.xpath('./div[@class="catalog-list"]/ul/li')
            # 3. 每章操作
            for chapter in chapter_list:
                chaptername=chapter.xpath('./a/text()')[0]
                chapter_url=chapter.xpath('./a/@href')[0]
                chapter_html=requests.get("https://book.sfacg.com/"+chapter_url,headers=headers)
                chapter_content=etree.HTML(chapter_html.text).xpath('/html/body/div[1]/div[3]/div/div/div[2]/div[2]/p/text()')
                if 0 ==len(chapter_content):# 判断是否是vip章节
                    return
                file.write(chaptername+'\n')
                for paragraph in chapter_content:
                    file.write('\t\t'+paragraph+'\n')
                    print(paragraph)
                file.write("\n\n\n")
                print("over!")
                # time.sleep(random.randint(1,10)+random.random())
    print("sucessfully!")

def NewFolder(name):# 新建文件夹;return 文件夹路径
    if not os.path.exists(name):
        os.makedirs(name)
    return name+"\\"

headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36"}
for id in range(300000,500000):
    url=f"https://book.sfacg.com/Novel/{id}/MainIndex/"
    GetOneBook(url)
    print(id)