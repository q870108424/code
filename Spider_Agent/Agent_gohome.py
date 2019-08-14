import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import re
import time
from urllib.parse import quote

class GOHOME:
    def __init__(self):
        self.url = Queue()
        self.rentpage = Queue()
        self.salepage = Queue()
        self.links = []
        self.items = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    def get_page(self):
        for i in range(1, 137):
            self.salepage.put(i)
        # for i in range(1, 106):
        #     self.rentpage.put(i)

    def get_url(self):
        while not self.salepage.empty():
            i = self.salepage.get()
            print(i,self.salepage.qsize())
            url=r'https://www.gohome.com.hk/%E8%B2%B7%E6%A8%93/?page={}'.format(i)
            response=requests.session().get(url=url,headers=self.headers)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div/ul//li/div/div[1]/div[3]/div[3]/div[2]/div/a/@href')
            linkss=tree.xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div/ul//li/div/div[1]/div[1]/a/@href')
            for link in links:
                link='https://www.gohome.com.hk/'+link
                self.links.append(link)
                print(link)
            for link in linkss:
                link = 'https://www.gohome.com.hk/' + link
                self.links.append(link)
                print(link)
            self.salepage.task_done()
    def get_rurl(self):
        while not self.rentpage.empty():
            i = self.rentpage.get()
            print(i,self.rentpage.qsize())
            url=r'https://www.gohome.com.hk/%E7%A7%9F%E6%A8%93/list/?page={}'.format(i)
            response=requests.session().get(url=url,headers=self.headers)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div/ul//li/div/div[1]/div[3]/div[3]/div[2]/div/a/@href')
            linkss = tree.xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div/ul//li/div/div[1]/div[1]/a/@href')
            for link in links:
                link = 'https://www.gohome.com.hk/' + link
                self.links.append(link)
                print(link)
            for link in linkss:
                link = 'https://www.gohome.com.hk/' + link
                self.links.append(link)
                print(link)
            self.rentpage.task_done()
    def saveurl(self):
        df = pd.DataFrame({'url': self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\gohome二手盘.xlsx', index=None)


    def run(self):
        # list1 = []
        # list2 = []
        # for i in range(10):
        #     t = threading.Thread(target=self.get_url)
        #     list1.append(t)
        # for t in list1:
        #     t.setDaemon(True)
        #     t.start()
        # for t in list1:
        #     t.join()
        # for i in range(10):
        #     t = threading.Thread(target=self.get_rurl)
        #     list2.append(t)
        # for t in list2:
        #     t.setDaemon(True)
        #     t.start()
        # for t in list2:
        #     t.join()
        # self.saveurl()
        list3=[]
        self.read_url()
        for i in range(10):
            t = threading.Thread(target=self.get_index)
            list3.append(t)
        for t in list3:
            t.setDaemon(True)
            t.start()
        # for t in list3:
        #     t.join()
        time.sleep(1300)
        self.save_inde()


    def read_url(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\gohome二手盘.xlsx').values.tolist()
        for row in df:
            row1=re.findall(r'property/(.*?)/',row[0])
            row2=re.findall(r'property/.*?/(.*?)/',row[0])
            num=re.findall(r'\d+',row[0])[0]
            one = quote(row1[0], 'utf-8')
            two = quote(row2[0], 'utf-8')
            url='https://www.gohome.com.hk/property/'+one+'/'+two+'/'+num
            self.url.put(url)
    def get_index(self,ret=1):
        while not self.url.empty():
            url=self.url.get()
            self.url.task_done()
            print(self.url.qsize(),url)
            try:
                response = requests.session().get(url=url, headers=self.headers)
                response.encoding = 'UTF-8'
                tree = html.fromstring(response.text)
                inde = tree.xpath('/html/body/div[1]/script[1]/text()')
            except Exception as e:
                if ret>4:
                    # self.url.task_done()
                    return self.get_index()
                else:
                    print('retring by %s' % ret)
                    time.sleep(5)
                    # self.url.task_done()
                    self.url.put(url)
                    return self.get_index(ret=ret + 1)
            if len(inde) > 0:
                inde=inde[0]
                dic1=re.findall('"organisations":\[(.*?)\]',inde)
                if len(dic1) > 0 :
                    dic1=eval(dic1[0]) if len(dic1)>0 else None
                    dic2=eval(re.findall('"listers":\[(.*?}})]',inde)[0])
                    company=dic1.get('name')
                    name=dic2.get('name')
                    card=dic2.get('license')
                    tel=dic2.get('contact').get('phones')[0].get('number')
                    try:
                        tel2=dic2.get('contact').get('phones')[1].get('number')
                    except Exception as e:
                        tel2=None
                    try:
                        email=dic2.get('contact').get('emails')[0]
                    except Exception as e:
                        email = None
                    print(name,card,company,tel,tel2,email)
                    item=[name,card,company,tel,tel2,email]
                    self.items.append(item)


    def save_inde(self):
        print('saving')
        df=pd.DataFrame(self.items,columns=['姓名','牌照','所屬公司','電話1','電話2','郵件'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\gohome經紀人.xlsx',index=None)
        print('profession')




if __name__ == '__main__':
    gohome=GOHOME()
    # gohome.get_page()
    gohome.run()
    # gohome.read_url()
    # gohome.get_index()
