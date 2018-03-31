#coding:utf-8
#! ‪C:\Developer\python36\python3.exe
import selenium
import selenium.webdriver
import lxml
import lxml.etree

url = 'http://news.bitauto.com/xinche/ssxc/'
driver = selenium.webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(3)
html = driver.page_source
myTree = lxml.etree.HTML(html)
divList = myTree.xpath('//div[@id="price_tab_ul"]//div')
for i in range(0,len(divList),2):
    print(divList[i].xpath('./ul//li[1]/a/text()'))
    print(divList[i].xpath('./ul//li[2]/a/text()'))
    print(divList[i].xpath('./ul//li[3]/text()'))
    print(divList[i].xpath('./div/a/img/@src'))
    print(divList[i].xpath('./div/a/@href'))

    # name = div.xpath('./ul//li[1]/a/text()')
    # price = div.xpath('./ul//li[2]/a/text()')
    # info = div.xpath('./ul//li[3]/text()')
    # imgUrl = div.xpath('./div/a/img/@src')
    # print(name,price,info,imgUrl)