from fake_useragent import UserAgent
import requests
from lxml import html
import pandas as pd
from queue import Queue


class Midygs:
    def __init__(self):
        self.ua = UserAgent()
        self.links = Queue()
        self.items = []
        self.link = []

    def get_url(self):
        for i in range(0, 16):
            headers = {
                'User-Agent': self.ua.random
            }
            url = r'http://oir.centanet.com/office/salesblogmain?postType=sell&floor=0&priceType=total&pageIndex={}&pageSize=9&sortBy=1&sortDirection=1&dateRange=16%2F05%2F2018+-+16%2F05%2F2019&region=0&isPropSearch=true&transSource=0&dept=2'.format(
                i)
            response = requests.session().get(url, headers=headers)
            tree = html.fromstring(response.text)
            links = tree.xpath('//div[@class="sales-iso"]/div[1]/a/@href')
            for link in links:
                link = 'http://oir.centanet.com' + link
                self.links.put(link)
                self.link.append(link)
            print(i, links)
        self.save2()

    def save(self):
        df = pd.DataFrame(
            self.items,
            columns=[
                '中文名',
                '英文名',
                '代理牌照',
                '電話1',
                '電話2',
                '電話3',
                'EMAIL',
                '分行地址',
                '所屬公司'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\中原寫字樓.xlsx')

    def save2(self):
        df = pd.DataFrame({'links': self.link})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\中原寫字樓網址.xlsx')

    def get_index(self):
        df = pd.read_excel(
            r'C:\Users\Administrator\Desktop\经纪人爬取\中原寫字樓網址.xlsx').values.tolist()
        for row in df:
            url = row[0]
            # url=self.links.get()
        # url=r'http://oir.centanet.com/industrial/salesblogdetail?licenseNo=S-263662'
            headers = {
                'User-Agent': self.ua.random
            }
            response = requests.session().get(url, headers=headers)
            tree = html.fromstring(response.text)
            chiname = tree.xpath(
                '//*[@id="panel"]/div[1]/div[2]/div/div[1]/span[last()]/text()')
            chiname = chiname[0] if len(chiname) > 0 else None
            card = tree.xpath(
                '//*[@id="panel"]/div[1]/div[3]/div/div[2]/div[2]/text()')
            card = card[0] if len(card) > 0 else None
            enname = tree.xpath(
                '//*[@id="panel"]/div[1]/div[3]/div/div[2]/div[1]/text()[2]')
            enname = enname[0].strip() if len(enname) > 0 else None
            tel = tree.xpath(
                '//*[@id="panel"]/div[1]/div[3]/div/div[2]/div[4]/div[2]/div[3]/div[1]//span/text()')
            email = tree.xpath(
                '//*[@id="panel"]/div[1]/div[3]/div/div[2]/div[4]/a/div[1]/span/text()')
            email = email[0] if len(email) > 0 else None
            adress = tree.xpath(
                '//div[@class="agentblog-info"]/div[4]/div[last()]/div/span/text()')
            print(adress)
            adress = adress[0] if len(adress) > 0 else None
            com = '中原寫字樓部'
            tel1 = tel[0].strip().replace(" ", "") if len(tel) > 0 else None
            tel2 = tel[1].strip().replace(" ", "") if len(tel) > 1 else None
            tel3 = tel[2].strip().replace(" ", "") if len(tel) > 2 else None
            item = [
                chiname,
                enname,
                card,
                tel1,
                tel2,
                tel3,
                email,
                adress,
                com]
            self.items.append(item)
            print(url)
            print(self.links.qsize(), item)


            # self.links.task_done()
if __name__ == '__main__':
    md = Midygs()
    md.get_url()
    md.get_index()
    md.save()
