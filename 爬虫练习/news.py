import requests#插入请求模块
from bs4 import BeautifulSoup#从BS4导入BeautifulSoup
import os#插入os模块用于文件处理
import re

def reqbs(url):#创建一个请求Response的函数
    res = requests.get(url)  # 利用requests获取网页的Rreponse
    res.encoding = 'utf-8'  # 改变网页的编码方式为utf-8，不然会乱码
    soup = BeautifulSoup(res.text, 'lxml')  # 利用BeautifulSoup解析网页，解析器用lxml
    return soup
soup = reqbs('http://news.sina.com.cn/china/')#新闻的主页
if not os.path.exists("D:/新闻"):#判断是否有这个文件夹
    os.makedirs("D:/新闻")#如果没有就创建
os.chdir("D:/新闻")# 切换该文件夹下面
#print(soup)这时候可以打印soup出来看看是不是我们要的
for news in soup.select('.news-item'):#筛选出新闻的URL
    if len(news.select('h2')) > 0 :#发现部分h2标签为空，剃掉h2标签下空的组合
        title = news.select('h2')[0].text.strip()#筛选新闻的标题
        title = re.sub('[\/:*?"<>|]', '', title)  #这几个符号？：‘’“”、Windows系统是不能创建文件夹的所以要替换掉
        href = news.select('a')[0]['href']#筛选出每个标题的链接
        time = news.select('.time')[0].text#取得新闻的时间
        #print(time, title, href)#打印出来看看是不是我们想要的
        Ros = reqbs(href)#利用新闻的链接取得每个新闻URL的Response
        article = []#建立一个空的列表用来存储新闻
        for p in Ros.select('#artibody p'):#筛选出新闻的具体内容
            #print(p.text)#打印出来看看是不是我们要的新闻
            article.append(p.text.strip())#将每一个找到的新闻内容加到我们的空列表里面去
        #print(article)
        fl = open(title+'.txt', 'w', encoding='utf-8')#打开一个以新闻标题命名的txt文件
        fl.write('\n'.join(article))#写入我们的新闻内容，并将列表中的每一个元素进行换行合并
        fl.close()#关闭文件
        article = []#将列表再次清空
        print(title, '下载完成')#表示一个新闻已经完成