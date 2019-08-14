import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import time

class Zymacau:
    def __init__(self):
        self.url = Queue()
        self.page = Queue()
        self.links = []
        self.items = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    def get_page(self):
        for i in range(1,120):
            self.page.put(i)
    def get_url(self):
        while not self.page.empty():
            i=self.page.get()
            print(i,self.page.qsize())
            url=r'https://mo.centanet.com/Project/Searchs?PageIndex=%s'%i
            response=requests.session().get(url=url,headers=self.headers)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('/html/body/div[3]/div[4]/div[3]/div/div/div[4]/div[1]/div[2]//a/@href')
            for link in links:
                link='https://mo.centanet.com'+link
                self.links.append(link)
                print(link)
        df = pd.DataFrame({'url': self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\澳門中原二手盘.xlsx', index=None)

    def read_url(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\澳門中原二手盘.xlsx').values.tolist()
        for row in df:
            url=row[0]
            self.url.put(url)

    def get_index(self,ret=1):
        while not self.url.empty():
        # url=r'https://mo.centanet.com/Project/BuildingDetails?id=5168'
            url=self.url.get()
            # url=r'https://mo.centanet.com/Project/BuildingDetails?id=6195'
            print(self.url.qsize())
            try:
                reponse = requests.session().get(url, headers=self.headers)
                tree = html.fromstring(reponse.text)
            except Exception as e:
                if ret>4:
                    self.url.task_done()
                    return self.get_index()
                else:
                    print('retring by %s' % ret)
                    time.sleep(5)
                    self.url.task_done()
                    self.url.put(url)
                    return self.get_index(ret=ret + 1)
            name=tree.xpath('/html/body/div[3]/div[4]/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[3]/div[1]/text()')
            name=name[0] if len(name)>0 else None
            pri = tree.xpath(
                '/html/body/div[3]/div[4]/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[3]//div/label[contains(text(),"職位級別")]/parent::*/text()')
            pri = pri[0] if len(pri)>0 else None
            company = tree.xpath(
                '/html/body/div[3]/div[4]/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[3]//div/label[contains(text(),"所屬分行")]/parent::*/text()')
            print(company)
            company = company[-1].strip() if len(company)>0 else None
            tel = tree.xpath(
                '/html/body/div[3]/div[4]/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[3]//div/label[contains(text(),"分行號碼")]/parent::*/label[last()]/text()')
            tel = tel[0].strip().replace("\r","").replace("\n","") if len(tel)>0 else None
            email = tree.xpath(
                '/html/body/div[3]/div[4]/div[3]/div/div[1]/div[2]/div/div[4]/div[2]/div[1]/div[3]//div/label[contains(text(),"Email")]/parent::*/text()')
            email = email[-1].strip() if len(email) > 0 else None
            item=[name,pri,company,tel,email]
            self.items.append(item)
            self.url.task_done()
            print(url, item)

    def save(self):
        print('保存中')
        columns=['聯絡人','职位','公司名','电话','郵件']
        df=pd.DataFrame(self.items,columns=columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\中原澳门经纪人.xlsx',index=None)
        print('保存完成')

    def run(self):
        self.read_url()
        list1 = []
        for i in range(10):
            t = threading.Thread(target=self.get_index)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()
        self.save()
if __name__ == '__main__':
    midland=Zymacau()
    # midland.get_page()
    midland.run()
    # midland.get_index()