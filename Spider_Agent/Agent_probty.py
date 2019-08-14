import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import time
class PRBTY:
    def __init__(self):
        self.links=[]
        self.page=Queue()
        self.url= Queue()
    def makepage(self):
        for i in range(1301):
            self.page.put(i)
    def get_url(self,ret=1):
        while not self.page.empty():
            i=self.page.get()
            print('第%s页'%i)
            url=r'http://w22.property.hk/property_search.php?p=%s&prop=&y=3&bldg=&sizeType=&size1=&size2=&saleType=&price1=&price2=&rent1=&rent2=&room=&e=&y=&pt=&dt=&isphoto=&greenform='%i
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
            try:
                reponse=requests.session().get(url,headers=headers)
                tree=html.fromstring(reponse.text)
                links=tree.xpath('//*[@id="proplist"]/div[1]/form/table//tr/td[last()]/div[1]/a/@href')
            except Exception as e:
                print('retring by %s'%ret)
                time.sleep(5)
                self.page.task_done()
                self.page.put(i)
                return self.get_url(ret=ret+1)
            for link in links:
                link='http://w22.property.hk'+link.replace(" ","")
                self.links.append(link)
                print(link)
            self.page.task_done()
        df=pd.DataFrame({'url':self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\property二手盘.xlsx',index=None)

    def run(self):
        list1=[]
        for i in range(10):
            t=threading.Thread(target=self.get_index)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()

    def get_index(self,ret=1):
        while not self.url.empty():
            print(self.url.qsize())
            url=self.url.get()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
            try:
                reponse = requests.session().get(url, headers=headers)
                reponse.encoding = "UTF-8"
                tree = html.fromstring(reponse.text)
                name = tree.xpath('//*[@id="property-contact"]/div[2]/table/tbody/tr[1]/td[2]/text()[1]')
                name=name[0] if len(name)>0 else None
                card = tree.xpath('//*[@id="property-contact"]/div[2]/table/tbody/tr[1]/td[2]/text()[2]')
                card = card[0] if len(card) > 0 else None
                company = tree.xpath('//*[@id="property-contact"]/div[2]/table/tbody/tr[1]/td[2]/text()[last()]')
                company = company[0] if len(company) > 0 else None
                tel = tree.xpath('//*[@id="property-contact"]/div[2]/table/tbody/tr[2]/td[2]/b/text()')
                tel = tel[0] if len(tel) > 0 else None
                item = [name,card,company,tel]
                self.links.append(item)
                print(url,item)
            except Exception as e:
                print('retring by %s' % ret)
                time.sleep(5)
                self.url.task_done()
                self.url.put(url)
                return self.get_url(ret=ret + 1)

    def save(self):
        print('保存中')
        df=pd.DataFrame(self.links,columns=['名字','牌照','所属公司','电话'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\property-经纪人.xlsx',index=None)
        print('保存完成')

    def readurl(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\property二手盘.xlsx').values.tolist()
        for row in df:
            url=row[0]
            self.url.put(url)

pb=PRBTY()
# pb.makepage()
pb.readurl()
pb.run()
pb.save()