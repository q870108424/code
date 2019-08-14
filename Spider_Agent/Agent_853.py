import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import time
class D853:
    def __init__(self):
        self.url=Queue()
        self.page=Queue()
        self.links=[]
        self.items=[]
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    def get_page(self):
        for i in range(1,1517):
            self.page.put(i)
    def get_url(self):
        while not self.page.empty():
            i=self.page.get()
            print(i,self.page.qsize())
            url=r'http://www.find853.com/index/Property_All.aspx?page=%s'%i
            response=requests.session().get(url=url,headers=self.headers)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('//*[@id="trshow1"]/td/table//tr/td[2]/table/tr/td/a/@href')
            for link in links:
                link='http://www.find853.com/index/'+link
                self.links.append(link)
                print(link)
        df = pd.DataFrame({'url': self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\853二手盘.xlsx', index=None)

    def read_url(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\853二手盘.xlsx').values.tolist()
        for row in df:
            url=row[0]
            self.url.put(url)
    def run(self):
        list1 = []
        self.get_page()
        for i in range(10):
            t = threading.Thread(target=self.get_url)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()

if __name__ == '__main__':
    d853=D853()
    d853.run()