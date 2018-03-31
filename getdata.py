#coding:utf-8
#! ‪C:\Developer\python36\python3.exe
import urllib
import urllib.request

import requests
import selenium
import selenium.webdriver
import time
import lxml
import lxml.etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
}
# url = 'http://news.bitauto.com/xinche/ssxc/'
url = 'http://car.bitauto.com/bentengb50/'
# driver = selenium.webdriver.Chrome()
# driver.get(url)
# driver.implicitly_wait(5)
# time.sleep(5)
html = requests.get(url,headers=headers).content.decode('utf-8')
print(html)
myTree = lxml.etree.HTML(html)
price1 = myTree.xpath('//a[@class="price"]/text()')[0]
price2 = myTree.xpath('//span[@class="price"]/text()')[0]
oil = myTree.xpath('//span[@class="data"]/text()')[0]
rateWay = myTree.xpath('//span[@class="data"]/text()')[1]
protect = myTree.xpath('//a[@class="lnk-bzl"]/text()')[0]
you = myTree.xpath('//span[@class="data"]/text()')[1]

print(price1)
print(price2)
print(oil)
print(rateWay)
print(protect)
print(you)

# for li in liList[1:]:
    # imgUrl = li.xpath('./div//div[1]//a[@class="openBox os_stat"]/img/@src')[0]
    # name = li.xpath('./div/div/a/img/@alt')[0]

    # age = li.xpath('./div//p[@class="user_info"]/text()')[0][:2]
    # tall = li.xpath('./div//p[@class="zhufang"]/span/text()')[0]
    # address = li.xpath('./div//p[1]/text()')[0][-2:]
#
#     print(imgUrl)
#     print(name)
#     print(age)
#     print(tall)
#     print(address)

