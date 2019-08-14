import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import time

class Ljgmacau:
    def __init__(self):
        self.url = Queue()
        self.page = Queue()
        self.links = []
        self.items = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    def get_page(self):
        for i in range(1,4):
            self.page.put(i)
    def get_url(self):
        while not self.page.empty():
            i=self.page.get()
            print(i,self.page.qsize())
            url=r'https://www.ricacorp.com.mo/rcproperty/search/d~s~g~sd~l~%s/na~na~na~na~na~na~na~na~na~na'%i
            response=requests.session().get(url=url,headers=self.headers,verify=False)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('//*[@id="searchResults"]//li/a[last()]/@href')
            for link in links:
                link='https://www.ricacorp.com.mo'+link
                self.links.append(link)
                print(link)
        df = pd.DataFrame({'url': self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\澳门利嘉閣二手盘.xlsx', index=None)

    def read_url(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\澳门利嘉閣二手盘.xlsx').values.tolist()
        for row in df:
            url=row[0]
            self.url.put(url)

    def get_index(self,ret=1):
        while not self.url.empty():
        # url=r'http://www.hkea.com.hk/pub/ListingServ?pid=H000366474'
            url=self.url.get()
            # url='https://www.ricacorp.com.mo/rcproperty/post/d~r/981d628d-5de2-40dd-86fc-5c79e05e7c1c'
            print(self.url.qsize())
            try:
                reponse = requests.session().get(url, headers=self.headers,verify=False)
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
            name=tree.xpath('//div[@class="mainAgent"]/strong/text()')
            name=name[0] if len(name)>0 else None
            tel=tree.xpath('//div[@class="mainAgent"]/div[2]/strong/text()')
            tel=tel[0] if len(tel)>0 else None
            card=tree.xpath('//div[@class="mainAgent"]/div[2]/span/text()')
            card=card[0] if len(card)>0 else None
            email=tree.xpath('//div[@class="mainAgent"]/a/text()')
            email=email[0] if len(email)>0 else None
            item=[name,tel,card,email]
            self.items.append(item)
            print(item)
            name2 = tree.xpath('//div[@class="otherAgent"]/div[2]/strong/text()')
            name2 = name2[0] if len(name2) > 0 else None
            tel2 = tree.xpath('//div[@class="otherAgent"]/div[2]/strong[3]/text()')
            tel2 = tel2[0] if len(tel2) > 0 else None
            card2 = tree.xpath('//div[@class="otherAgent"]/div[2]/span/text()')
            card2 = card2[0] if len(card2) > 0 else None
            email2 = tree.xpath('//div[@class="otherAgent"]/a/text()')
            email2 = email2[0] if len(email2) > 0 else None
            item2 = [name2, tel2, card2, email2]
            self.items.append(item2)
            self.url.task_done()
            print(item2)

    def run(self):
        list1 = []
        self.read_url()
        for i in range(1):
            t = threading.Thread(target=self.get_index)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()
        self.save()

    def save(self):
        print('保存中')
        columns=['聯絡人','電話','牌照','郵件']
        df=pd.DataFrame(self.items,columns=columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\澳门利嘉閣经纪人.xlsx',index=None)
        print('保存完成')

if __name__ == '__main__':
    ljg=Ljgmacau()
    # ljg.get_page()
    ljg.run()
    # ljg.get_index()