import requests
from lxml import html
from queue import Queue
import pandas as pd
from multiprocessing import Process
import time
import threading
import os
from urllib.parse import urlparse
from urllib.parse import urljoin
class Spider:
    def __init__(self,info,inde_info,index_items):
        self.url = Queue()
        self.page = Queue()
        self.links = []
        self.inde_info=inde_info
        self.items = []
        self.info=info
        self.url_finish = False
        self.parser_html = False
        self.index_items=index_items
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    def get_page(self):
        page=self.info.get('page')
        for i in range(1,page+1):
            self.page.put(i)
    def get_url(self):
        sta=self.info.get('test_status')
        if sta == True:
            i=1
            print('测试-爬取')
            urls = self.info.get('test_url')
            for url in urls:
                print('爬取-',url)
                response = requests.session().get(url=url, headers=self.headers)
                response.encoding = 'UTF-8'
                tree = html.fromstring(response.text)
                xp = self.info.get('xpath')
                links = tree.xpath(xp)
                for link in links:
                    hos = self.info.get('url')
                    l = urlparse(hos)
                    host = str(l.scheme) + '://' + str(l.netloc)
                    link = urljoin(host,link)
                    if 'javascript' not in link:
                        self.links.append(link)
                        self.url.put(link)
                        print(link)
            df = pd.DataFrame({'url': self.links})
            name = self.info.get('name')
            df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\【测试】%s二手盘.xlsx' % name, index=None)
        else:
            while not self.page.empty():
                i=self.page.get()
                print('第%s页,剩余%s'%(i,self.page.qsize()))
                url=self.info.get('url')%i
                response=requests.session().get(url=url,headers=self.headers)
                response.encoding='UTF-8'
                tree=html.fromstring(response.text)
                xp=self.info.get('xpath')
                links=tree.xpath(xp)
                for link in links:
                    hos = self.info.get('url')
                    l = urlparse(hos)
                    host = str(l.scheme) + '://' + str(l.netloc)
                    link = urljoin(host, link)
                    if 'javascript' not in link:
                        self.links.append(link)
                        self.url.put(link)
                        print(link)
            df = pd.DataFrame({'url': self.links})
            name=self.info.get('name')
            path=self.inde_info.get('path')
            urlpath=path+'/'+name+'二手盘.xlsx'
            df.to_excel(urlpath, index=None)


    def read_url(self):
        name = self.info.get('name')
        path = self.inde_info.get('path')
        urlpath = path + '/' + name + '二手盘.xlsx'
        st=os.path.exists(urlpath)
        if not st:
            time.sleep(2)
            return self.read_url()
        else:
            df=pd.read_excel(urlpath).values.tolist()
            for row in df:
                url=row[0]
                self.url.put(url)

    def get_index(self,ret=1):
        while not self.url.empty():
            url=self.url.get()
            print(self.url.qsize())
            try:
                reponse = requests.session().get(url, headers=self.headers)
                reponse.encoding='UTF-8'
                tree = html.fromstring(reponse.text)
            except Exception as e:
                if ret>4:
                    self.url.task_done()
                    print('重连超过4次，抛弃此url')
                    return self.get_index()
                else:
                    print('重连第%s次' % ret)
                    time.sleep(3)
                    self.url.task_done()
                    self.url.put(url)
                    return self.get_index(ret=ret + 1)
            item=[]
            for i in list(self.index_items.keys()):
                ind=tree.xpath(self.index_items.get(i))
                ind = ind[0].strip().replace("\r","").replace("\n","") if len(ind) > 0 else None
                item.append(ind)
            self.items.append(item)
            print(url,'\n',item)
        if self.url_finish==True and self.url.empty() is True:
            return
        elif self.url_finish==False:
            time.sleep(1)
            return self.get_index()

    def save(self):
        path = self.inde_info.get('path')
        name = self.info.get('name')
        allpath = path + '/' + name + '-经纪人.xlsx'
        columns = list(self.index_items.keys())
        df = pd.DataFrame(self.items, columns=columns)
        df.to_excel(allpath, index=None)
        if self.url_finish==True:
            print('全部网页解析完毕')
        elif self.url_finish==False:
            time.sleep(2)
            return self.save()



    def run_tourl(self):
        self.get_page()
        list1 = []
        thr=self.info.get('thread')
        for i in range(thr):
            t = threading.Thread(target=self.get_url)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()
        self.url_finish=True
        print('已导出表格')

    def run_toinde(self):
        sta = self.inde_info.get('test_status')
        if sta == True:
            self.url_finish == True
            urls = self.inde_info.get('test_url')
            for url in urls:
                self.url.put(url)
        list1 = []
        thr=self.info.get('thread')
        for i in range(thr):
            t = threading.Thread(target=self.get_index)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()
        self.parser_html=True


    def run_all(self):
        p1=threading.Thread(target=self.run_tourl)
        p2=threading.Thread(target=self.run_toinde)
        p3=threading.Thread(target=self.save)
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p3.join()
        print('全部爬取且保存完成')


class items(dict):
    """A class used to store data"""