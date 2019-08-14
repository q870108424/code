import requests
from lxml import html
import pandas as pd
import time
from selenium import webdriver
class Midyuan:
    def __init__(self):
        self.number=[]
        self.loca=[]
        self.items=[]
    def makurl(self,cod,loca):
        url=r'http://hk.centanet.com/findproperty/zh-HK/Home/AgentDetail?sid=%s'%cod
        print(url,loca)
        # self.getindex(url,loca)
        self.get_index(url)
    def getindex(self,url,loca):
        # url=r'http://hk.centanet.com/findproperty/zh-HK/Home/AgentIndex?mktid=HK&scopeid=102'
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
        }
        web_driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')
        web_driver.get(url)
        time.sleep(5)
        numbers=web_driver.find_elements_by_xpath('//div[@class="SearchResult_Row"]/div[3]/p[3]')
        for number in numbers:
            self.number.append(number.text)
            self.loca.append(loca)
            print(number.text)
        df=pd.DataFrame({'number':self.number,'loca':self.loca})
        web_driver.close()
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\number-kl.xlsx', index=None)
        return df
    def get_index(self,url,retires=1):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            }
            response=requests.session().get(url,headers=headers)
        except Exception as e:
            print('重連第%s次'%retires)
            return self.get_index(url,retires=retires+1)
        tree=html.fromstring(response.text)
        names=tree.xpath('/html/body/div[11]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/p[1]/strong/text()[2]')
        name=names[0].replace("\r","").replace("\n","").strip() if names!=[] else None
        ennames=tree.xpath('/html/body/div[11]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/p[1]/strong/text()[1]')
        enname = ennames[0].replace("\r", "").replace("\n", "").strip() if ennames != [] else None
        # cards=tree.xpath('/html/body/div[11]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/p[1]/text()')
        # card = cards[0].replace("\r", "").replace("\n", "").strip() if cards != [] else None
        adresss=tree.xpath('/html/body/div[11]/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div/text()')
        adress = adresss[0].replace("\r", "").replace("\n", "").strip() if adresss != [] else None
        tels = tree.xpath('/html/body/div[11]/div/div[2]/div[2]/div/div/div[1]/div[2]/p/strong/text()')
        tel = tels[0].replace("\r", "").replace("\n", "").strip().replace(" ", "") if tels != [] else None
        com = '中原地產'
        email=''
        tel2=''
        card=cod
        item=[enname,name,tel,tel2,email,com,adress,card]
        cloumns=['英文名','中文名','電話1','電話2','Email','所屬公司','所屬分行','代理牌照']
        self.items.append(item)
        print(item)
        df=pd.DataFrame(self.items,columns=cloumns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\中原-index.xlsx', index=None)
if __name__ == '__main__':
    mid=Midyuan()
    df = pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\中原\number.xlsx').values.tolist()
    for code in df:
        cod=code[0]
        loca=code[1]
        print(cod,loca)
        mid.makurl(cod,loca)

