import requests
from queue import Queue
import re
import urllib
from lxml import html
import pandas as pd
import threading
class spier591:

    def __init__(self):
        self.sale_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://sale.591.com.hk/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }  # 用于售盘POST
        self.rent_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie':'_ga=GA1.3.825760789.1548208707; __auc=1729cf52168786e1514859de3bf; userUnique=eb98056023fef005fc6fc8ce4b1bdd699507ac1d; think_template=default; _fbp=fb.2.1552446418790.1513396267; rongCloudUnicode=717479d34fe7af72404825e0f74c511044381014; _gid=GA1.3.1934852734.1557711570; PHPSESSID=MjExMjAzNTU1ODVjZDkwOTA1OTE4MGU3LjY0NTI0; think_language=zh-hk; __asc=f4c46c5816ab05d583b7985ee7e; houseviews=1791433%7C2374633%7C2303737%7C2378478%7C2256747%7C1705381%7C1796834%7C1675154%7C1802873%7C1760772%7C1632686%7C2375714%7C2383765%7C2366651%7C2366650%7C2381958%7C1749440%7C1803191%7C1793388%7C1593447%7C1802088%7C1750680%7C1806172%7C1806159%7C1806153%7C1806792%7C1806841%7C1807084%7C1643855%7C1803866%7C1803104%7C2390335%7C2382119%7C2390114%7C1808536%7C1806011%7C1709281%7C1809968%7C2383305%7C2390473%7C2809968%7C1792218%7C1751345%7C1810447%7C1806225%7C1812529%7C1810486%7C1813076%7C1811402%7C1813074%7C1745237%7C1809333%7C1813999%7C1814299%7C1813383%7C1804780%7C1812485%7C2390461%7C1723496%7C1814737%7C1810572; DETAIL=%7B%221%22%3A%5B%22812485%22%2C%22723496%22%2C%22810572%22%5D%2C%222%22%3A%5B%22390461%22%5D%7D; _gat=1; _gat_rent=1',
            'Host': 'rent.591.com.hk',
            'Referer': 'https://rent.591.com.hk/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }  # 用于租盘POST
        self.html_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        self.post_sale = r'https://sale.591.com.hk/?m=home&c=search&a=rslist&v=new&type=2&region=6&hasimg=1&searchtype=1&p=1&role='
        self.post_rent = r'https://rent.591.com.hk/?m=home&c=search&a=rslist&v=new&type=1&region=6&hasimg=1&searchtype=1&p=3&role='
        self.rentpage_queue = Queue()  # 页码
        self.salepage_queue = Queue()
        self.url_queue = Queue()  # 实例化三个队列，用来存放内容
        self.html_queue = Queue()
        self.index_queue = Queue()
        self.items=[]
        self.url=[]
        self.columns=['姓名','電話','固話','郵箱','代理牌照','所屬公司','分行地址']
    def get_page(self):
        salepages = []
        req = urllib.request.Request(self.post_sale, headers=self.sale_headers)
        response = urllib.request.urlopen(req)
        text = response.read()
        text = text.decode().replace("\/", "/")
        page = re.findall(r'data-page=(\d+)', text)
        for salepage in page:
            salepages.append(int(salepage))
        salepage = max(salepages)
        print('售盘%s页' % salepage)
        for a in range(1, salepage + 1):
            self.salepage_queue.put(a)
        rentpages = []
        req = urllib.request.Request(self.post_rent, headers=self.rent_headers)
        response = urllib.request.urlopen(req)
        text = response.read()
        text = text.decode().replace("\/", "/")
        page = re.findall(r'data-page=(\d+)', text)
        for rentpage in page:
            rentpages.append(int(rentpage))
        rentpage = max(rentpages)
        print('租盘%s页' % rentpage)
        for b in range(1, rentpage + 1):
            self.rentpage_queue.put(b)
    def salepost(self):
        while not self.salepage_queue.empty():
            salepage=self.salepage_queue.get()
            print('591-正在爬取售盘第%s页' % salepage)
            surl = r'https://sale.591.com.hk/?m=home&c=search&a=rslist&v=new&type=2&region=6&hasimg=1&searchtype=1&p=%s&role=' % salepage
            req = urllib.request.Request(surl, headers=self.sale_headers)
            response = urllib.request.urlopen(req)
            text = response.read()
            text = text.decode().replace("\/", "/")
            links = re.findall(r'https://sale.591.com.hk/sale-detail-\d+.html\?z=[0-9\_]+', text)
            for link in links:
                self.url_queue.put(link)
                self.url.append(link)
            self.salepage_queue.task_done()

    def rentpost(self):
        while not self.rentpage_queue.empty():
            rentpage = self.rentpage_queue.get()
            print('591-正在爬取租盘第%s页' % rentpage)
            rurl = r'https://rent.591.com.hk/?m=home&c=search&a=rslist&v=new&type=1&region=6&hasimg=1&searchtype=1&p=%s&role=' % rentpage
            req = urllib.request.Request(rurl, headers=self.rent_headers)
            response = urllib.request.urlopen(req)
            text = response.read()
            text = text.decode().replace("\/", "/")
            links = re.findall(r'https://rent.591.com.hk/rent-detail-\d+.html\?z=[0-9\_]+', text)
            for link in links:
                self.url_queue.put(link)
                self.url.append(link)
            self.rentpage_queue.task_done()

    def get_index(self,retires=1):
        while not self.url_queue.empty():
            print(self.url_queue.qsize())
            url=self.url_queue.get()
            try:
                response=requests.session().get(url,headers=self.html_headers)
            except Exception as e:
                print('重連')
                self.url_queue.put(url)
                return self.get_index(retires=retires+1)
            tree=html.fromstring(response.text)
            status=tree.xpath('//div[@class="name"]/span/text()')
            statu=status[0].replace("(","").replace(")","") if len(status)>0 else None
            if statu=='業主':
                print(url,'業主盤')
                self.url_queue.task_done()
            else:
                name = tree.xpath('//div[@class="name"]/text()')
                name = name[0].replace(" ", "").replace("\n", "") if len(name) > 0 else None
                tel = tree.xpath('//div[@class="new-tel"]/text()')
                tel = tel[0].replace(" ", "").replace("\n", "") if len(tel) > 0 else None
                gtel=tree.xpath('//div[@class="bottom"]/ul/li[1]/text()')
                gtel = gtel[0].replace(" ", "").replace("\n", "") if len(gtel) > 0 else None
                email=tree.xpath('//div[@class="bottom"]/ul/li[2]/text()')
                email = email[0].replace(" ", "").replace("\n", "") if len(email) > 0 else None
                card=tree.xpath('//div[@class="bottom"]/ul/li[3]/text()')
                card = card[0].replace(" ", "").replace("\n", "") if len(card) > 0 else None
                com=tree.xpath('//div[@class="bottom"]/ul/li[4]/a/text()')
                com = com[0].replace(" ", "").replace("\n", "") if len(com) > 0 else None
                adress=tree.xpath('//div[@class="bottom"]/ul/li[4]/a/@title')
                adress = adress[0].replace(" ", "").replace("\n", "") if len(adress) > 0 else None
                item=[name,tel,gtel,email,card,com,adress]
                self.items.append(item)
                print(url,item)
                self.url_queue.task_done()
    def save(self):
        print('保存……')
        df=pd.DataFrame(self.items,columns=self.columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\591.xlsx',index=None)

    def saveurl(self):
        df = pd.DataFrame({'url':self.url})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\591二手盤.xlsx', index=None)

    def run(self):
        self.get_page()
        post_list = []
        thread_list=[]
        for i in range(10):
            thread_rentpost = threading.Thread(target=self.rentpost)
            thread_salepost = threading.Thread(target=self.salepost)
            post_list.append(thread_rentpost)
            post_list.append(thread_salepost)
        for t in post_list:
            t.setDaemon(True)
            t.start()
        for t in post_list:
            t.join()
        self.saveurl()
        for i in range(10):
            thread_parse=threading.Thread(target=self.get_index)
            thread_list.append(thread_parse)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join()
        self.save()
if __name__ == '__main__':
    sp=spier591()
    sp.run()