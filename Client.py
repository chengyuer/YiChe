#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import time  #随机数，时间
from queue import Queue #队列
import gevent
import gevent.monkey
import selenium.webdriver
import requests
import lxml
from lxml import etree
import urllib.request
import urllib

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}

def getData(res,result):
    name = res['name']
    topPrice=res['topPrice']
    date=res['date']
    imgUrl=res['imgUrl']
    carUrl=res['carUrl']
    fileName = 'D:/pythonProject/CrawlProject21/yicheFenBuShi/imgs/'+name+'.jpg'
    downImg(fileName, imgUrl)
    html = requests.get(carUrl, headers=headers).content.decode('utf-8')
    myTree = lxml.etree.HTML(html)
    try:
        price1 = myTree.xpath('//a[@class="price"]/text()')[0]
        price2 = myTree.xpath('//span[@class="price"]/text()')[0]
        oil = myTree.xpath('//span[@class="data"]/text()')[0]
        rateWay = myTree.xpath('//span[@class="data"]/text()')[1]
        protect = myTree.xpath('//a[@class="lnk-bzl"]/text()')[0]
        you = myTree.xpath('//span[@class="note"]/text()')[0]
        carDict = {'name':name,'topPrice':topPrice,'countryPrice':price1,'factoryPrice':price2,'pailiang':oil,'way':rateWay,'youhao':you,'date':date,'protect':protect}
        result.put(carDict)
        print('put:'+name)
    except:
        pass


def downImg(filePath,imgUrl):
    url = imgUrl
    urllib.request.urlretrieve(url, filename=filePath)

if __name__=="__main__":
    QueueManger.register("get_task")  # 注册函数调用服务器
    QueueManger.register("get_result")
    manger=QueueManger(address=("127.0.0.1",8848),authkey=123456)
    manger.connect()  #链接服务器
    task= manger.get_task()
    result =manger.get_result()  # 任务，结果

    for  i  in range(10000):#不间断的从服务端拿任务
        res = task.get()
        getData(res,result)