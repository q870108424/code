import requests
import time
import pandas as pd
from lxml import html
import re
import json
from queue import Queue
import threading
class ft:
    def __init__(self):
        self.ls=Queue()
        self.link=[]

    def geturl(self,ret=1):
        while not self.ls.empty():
            i=self.ls.get()
            time.sleep(0.5)
            url=r'https://www.squarefoot.com.hk/%E7%A7%9F%E6%A8%93/list/?page={}'.format(i)
            print(url)
            headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            try:
                response=requests.session().get(url,headers=headers)
            except Exception as e:
                print('重连-%s'%i)
                time.sleep(5)
                self.ls.put(i)
                return self.geturl(ret=ret+1)
            tree=html.fromstring(response.text)
            link=tree.xpath('//*[@id="app"]/div/div/div[2]/div[3]/div[1]/div/ul//li/div/div[3]/div[3]/div[2]/div/a/@href')
            if link !=[]:
                for li in link:
                    self.link.append(li)
                self.ls.task_done()
            else:
                self.ls.task_done()

    def save(self):
        print('saving……')
        df=pd.DataFrame(self.link,columns=['中文名','英文名','listerLicense','agencyLicense','所屬公司','電話1','電話2'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\squarefoot.xlsx',index=None)

    def get_html(self):
        while not self.ls.empty():
            url=self.ls.get()
            print(self.ls.qsize())
            en = re.compile(r'[\u0061-\u007a,\u0020]')
            chi = re.compile(r'[\u4e00-\u9fa5,\u0020]')
            response=requests.session().get(url)
            response.encoding='UTF-8'
            dic=re.findall('{"listerId".*?"label"',response.text)
            for i in dic:
                card=re.findall('agencyLicense":"(.*?)",',i)
                card = card[0] if len(card)>0 else None
                listerLicense=re.findall('listerLicense":"(.*?)",',i)
                listerLicense = listerLicense[0] if len(listerLicense) > 0 else None
                name=re.findall('listerName":"(.*?)",',i)
                name = name[0] if len(name) > 0 else None
                enname="".join(en.findall(name.lower()))
                chiname="".join(chi.findall(name.lower()))
                com=re.findall('agencyName":"(.*?)",',i)
                com = com[0] if len(com) > 0 else None
                phone=re.findall('(\d{8,11})',i)
                phone1 = phone[0] if len(phone) > 0 else None
                phone2= phone[1] if len(phone) > 1 else None
                # a=json.load(i)
                item=[chiname,enname,listerLicense,card,com,phone1,phone2]
                print(phone1,phone2,'\n',url)
                self.link.append(item)
            self.ls.task_done()


    def page(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\sqfoot\squarefoot-buy.xlsx').values.tolist()
        for row in df:
            url='https://www.squarefoot.com.hk'+row[0]
            self.ls.put(url)

    def run(self):
        t=[]
        self.page()
        for i in range(10):
            s=threading.Thread(target=self.get_html)
            t.append(s)
        for a in t:
            a.setDaemon(True)
            a.start()
        for a in t:
            a.join()
        self.save()
if __name__ == '__main__':
    ff=ft()
    # ff.run()
    # save(ls)
    ff.run()