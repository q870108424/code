import requests
from lxml import html
from queue import Queue
import pandas as pd
import threading
import time
class HKET:
    def __init__(self):
        self.url=Queue()
        self.page=Queue()
        self.links=[]
        self.items=[]
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    def get_page(self):
        for i in range(1,107):
            self.page.put(i)
    def get_url(self):
        while not self.page.empty():
            i=self.page.get()
            print(i,self.page.qsize())
            url=r'http://www.hkea.com.hk/pub/ListingServ?currPage=%s'%i
            response=requests.session().get(url=url,headers=self.headers)
            response.encoding='UTF-8'
            tree=html.fromstring(response.text)
            links=tree.xpath('//*[@id="box"]/div[4]/div[3]/div[1]/div[2]/div[2]//div/div/a/@href')
            for link in links:
                link='http://www.hkea.com.hk'+link
                self.links.append(link)
                print(link)
        df = pd.DataFrame({'url': self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\hket二手盘.xlsx', index=None)

    def read_url(self):
        df=pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\hket二手盘.xlsx').values.tolist()
        for row in df:
            url=row[0]
            self.url.put(url)


    def get_index(self,ret=1):
        while not self.url.empty():
        # url=r'http://www.hkea.com.hk/pub/ListingServ?pid=H000366474'
            url=self.url.get()
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
            companys = tree.xpath('//*[@id="box"]/div[4]/div[2]/div[2]/div[1]/div[2]/div[2]/text()')
            if companys != []:
                name = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"聯絡人")]/text()')
                name = name[0].split("：")[-1].strip() if len(name)>0 else None
                tel = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"電 　話")]/text()')
                tel = tel[0].split("：")[-1].strip() if len(tel) > 0 else None
                email = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"電 　郵")]/a/text()')
                email = email[0].split("：")[-1].strip() if len(email) > 0 else None
                comname = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"公司名稱")]/text()')
                comname = comname[0].split("：")[-1].strip() if len(comname) > 0 else None
                comcard = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"牌照號碼")]/text()')
                comcard = comcard[0].split("：")[-1].strip() if len(comcard) > 0 else None
                comtel = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"電 話")]/text()')
                comtel = comtel[0].split("：")[-1].strip() if len(comtel) > 0 else None
                comemail = tree.xpath('//div[@class="xq_lxzl"]//div//p[contains(text(),"電 郵")]/a/text()')
                comemail = comemail[0].split(":")[-1].strip() if len(comemail) > 0 else None
                dailiname = tree.xpath('//div[@class="xq_lxzl"]/div[3]//p[contains(text(),"代理")]/text()')
                dailiname = dailiname[0].split("：")[-1].strip() if len(dailiname) > 0 else None
                dailicard = tree.xpath('//div[@class="xq_lxzl"]/div[3]//p[contains(text(),"牌照號碼")]/text()')
                dailicard = dailicard[0].split("：")[-1].strip() if len(dailicard) > 0 else None
                dailitel = tree.xpath('//div[@class="xq_lxzl"]/div[3]//p[contains(text(),"電 話")]/text()')
                dailitel = dailitel[0].split("：")[-1].strip() if len(dailitel) > 0 else None
                item=[name,tel,email,comname,comcard,comtel,comemail,dailiname,dailicard,dailitel]
                self.items.append(item)
                self.url.task_done()
                print(url,item)
    def save(self):
        print('保存中')
        columns=['聯絡人','電話','郵件','公司名','公司牌照','公司電話','公司郵件','代理人','代理牌照','代理電話']
        df=pd.DataFrame(self.items,columns=columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\hket-经纪人.xlsx',index=None)
        print('保存完成')
    def run(self):
        list1 = []
        for i in range(10):
            t = threading.Thread(target=self.get_index)
            list1.append(t)
        for t in list1:
            t.setDaemon(True)
            t.start()
        for t in list1:
            t.join()
if __name__ == '__main__':
    hket=HKET()
    hket.read_url()
    hket.run()
    hket.save()