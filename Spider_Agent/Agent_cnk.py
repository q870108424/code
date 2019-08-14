import requests
from lxml import html
import pandas as pd
from queue import Queue
import threading
import time
from fake_useragent import UserAgent

#科一代理
class kone:
    def __init__(self):
        self.lins = []
        self.pages = Queue()
        self.ua = UserAgent()

    def get_url(self, ret=1):
        while not self.pages.empty():
            i = self.pages.get()
            url = r'http://cnp.hk/property.php?p=%s&o=&e=&y=3&d=ALL&t=&b=&s=&c=&n=&h=&pt=&v=&agtcode=' % i
            try:
                response = requests.session().get(url)
            except Exception as e:
                print('重連')
                self.pages.put(i)
                return self.get_url(ret=ret + 1)
            tree = html.fromstring(response.text)
            links = tree.xpath(
                '//div[@id="proplist"]/div[2]/table//tr/td[1]/a/@href')
            for link in links:
                print(i, link)
                link = 'http://cnp.hk/' + link
                self.lins.append(link)
            self.pages.task_done()

    def save(self):
        df = pd.DataFrame(self.lins, columns=['姓名', '牌照', '英文名', '電話'])
        df.to_excel(
            r'C:\Users\Administrator\Desktop\经纪人爬取\科一4.xlsx',
            index=None)
        print('保存了')

    def page(self):
        df = pd.read_excel(
            r'C:\Users\Administrator\Desktop\经纪人爬取\工作簿1.xlsx').values.tolist()
        for row in df:
            i = row[0]
            self.pages.put(i)

    def get_html(self, ret=1):
        while not self.pages.empty():
            time.sleep(2)
        # url=r'http://cnp.hk/property_detail.php?ref=B7835760'
            url = self.pages.get()
            headers = {'User-Agent': self.ua.random}
            try:
                response = requests.session().get(url, headers=headers)
                response.encoding = "UTF-8"
            except Exception as e:
                if ret < 4:
                    print('重連', ret)
                    self.pages.task_done()
                    self.pages.put(url)
                    return self.get_html(ret=ret + 1)
                else:
                    self.pages.task_done()
                    continue
            tree = html.fromstring(response.text)
            index = tree.xpath(
                '//*[@id="main-content"]/div/div/div/table/tr/td[1]/div/div/div[1]/div[2]/div[2]/table//tr/td[2]/text()')
            if index == []:
                index = tree.xpath(
                    '//*[@id="main-content"]/div/div/div/table/tr/td[1]/div/div/div[1]/div[3]/div[2]/table//tr/td[2]/text()')
            if len(index) == 4:
                tel = index[-1]
                ename = index[2]
                card = index[1]
                name = index[0]
            elif len(index) > 0:
                tel = index[-1] if len(index) > 0 else None
                ename = index[-2].strip() if len(index) > 2 else None
                name = index[-3] if len(index) > 3 else None
                card = None
            else:
                if ret < 4:
                    self.pages.task_done()
                    self.pages.put(url)
                    return self.get_html(ret=ret + 1)
                else:
                    self.pages.task_done()
                    continue
            item = [name, card, ename, tel]
            self.lins.append(item)
            self.pages.task_done()
            print(self.pages.qsize(), item, url)
        if self.pages.qsize() == 0:
            self.save()

    def run(self):
        thlist = []
        self.page()
        for i in range(10):
            pagelist = threading.Thread(target=self.get_html)
            thlist.append(pagelist)
        for t in thlist:
            t.setDaemon(True)
            t.start()
        for t in thlist:
            t.join()
        self.save()


if __name__ == '__main__':
    kone = kone()
    # kone.get_html()
    kone.run()
