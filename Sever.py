#coding:utf-8
import multiprocessing  #分布式进程
import multiprocessing.managers #分布式进程管理器
import random,time  #随机数，时间
from queue import Queue #队列
import pymongo
from selenium.webdriver import DesiredCapabilities
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree


task_queue=Queue() #任务
result_queue=Queue() #结果

def  return_task(): #返回任务队列
    return task_queue
def return_result(): #返回结果队列
    return   result_queue

class  QueueManger(multiprocessing.managers.BaseManager):#继承，进程管理共享数据
    pass

if __name__=="__main__":
    multiprocessing.freeze_support()#开启分布式支持
    QueueManger.register("get_task",callable=return_task)#注册函数给客户端调用
    QueueManger.register("get_result", callable=return_result)
    manger=QueueManger(address=("127.0.0.1",8848),authkey=123456) #创建一个管理器，设置地址与密码
    manger.start() #开启
    task,result=manger.get_task(),manger.get_result() #任务，结果

    url = "http://news.bitauto.com/xinche/ssxc/"
    myCon = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = myCon['yicheFenBuShi']
    coll = db['data']
    # dcap = dict(DesiredCapabilities.PHANTOMJS)  # 处理无界面浏览器
    # dcap["phantomjs.page.settings.userAgent"] = (
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0")
    # driver = selenium.webdriver.PhantomJS(
    #     executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe",
    #     desired_capabilities=dcap)
    driver = selenium.webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(3)
    print('go Url')
    html = driver.page_source
    myTree = lxml.etree.HTML(html)
    divList = myTree.xpath('//div[@id="price_tab_ul"]//div')
    for i in range(0, len(divList), 2):
        name = divList[i].xpath('./ul//li[1]/a/text()')[0]
        topPrice = divList[i].xpath('./ul//li[2]/a/text()')[0]
        date = divList[i].xpath('./ul//li[3]/text()')[0]
        imgUrl = divList[i].xpath('./div/a/img/@src')[0]
        carUrl = divList[i].xpath('./div/a/@href')[0]
        carDict = {'name':name,'topPrice':topPrice,'date':date,'imgUrl':imgUrl,'carUrl':carUrl}#相当于创建一个对象
        task.put(carDict)#将每个对象传给客户端

    print ("waitting for------")

    for  i  in range(10000):#不间断的从客户端提取数据
        res=result.get()
        coll.insert(res)   #存入mongodb
        print ("get data",res)

    manger.shutdown()#关闭服务器

