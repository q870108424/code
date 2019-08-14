from queue import Queue
import urllib
import requests
import re
import time
import pandas as pd
from lxml import html
import threading
class Hse28:
    def __init__(self):
        self.information=[]
        self.linss=[]
        self.items=[]
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                   'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
                   'Origin': 'https://www.28hse.com', 'Referer': 'https://www.28hse.com/buy',
                   'Content-Type': 'application/x-www-form-urlencoded'}#用于发送POST请求
        self.headers_= {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}#用于获取页面信息
        self.url_queue = Queue()  # 实例化三个队列，用来存放内容
        self.html_queue = Queue()
        self.index_queue = Queue()
        self.sale_queue =Queue()
        self.rent_queue = Queue()

    def page(self):
        for i in range(1,2800):
            self.sale_queue.put(i)
        for i in range(1,1900):
            self.rent_queue.put(i)

    def rentpost(self):
        url = r'https://www.28hse.com/utf8/search3_ajax.php'
        while not self.rent_queue.empty():
            p=self.rent_queue.get()
            print('28hse-正在爬取最新租盘链接', p)
            formdata = {
                "the_alldata": "s_order=0&s_order_direction=0&s_type=0&s_sellrent=2&s_sellrange=0&s_sellrange_l=0&s_sellrange_h=0&s_rentrange=0&s_rentrange_l=0&s_rentrange_h=0&s_source=2&s_roomno=0&s_area=0&s_area_l=0&s_area_h=0&s_cached_fav=0&s_stored_fav=0&s_page=%s&s_myrelated=0&s_cat_child=0&s_restore_search_codition=0&s_global_tag=0&s_viewmode=0&s_age=0&s_age_l=0&s_age_h=0&s_rent=0&stypeg_1_mode=1&stypeg_1_18=1&stypeg_1_17=1&stypeg_1_10=1&stypeg_1_11=1&stypeg_1_5=1&stypeg_1_7=1&stypeg_1_6=1&stypeg_1_19=1&stypeg_8_16=0&s_keywords=&input_low=&input_high=&s_area_buildact=1&input_low=&input_high=&input_low=&input_high=" % p,
                "action": 200
            }
            data = urllib.parse.urlencode(formdata).encode(encoding='UTF-8')
            try:
                response = requests.session().post(url, data=data, headers=self.headers)
                link = re.findall(r'https://www.28hse.com/rent-property-\d+.html', response.text.replace("\/", "/"))
                link = list(set(link))
                for l in link:
                    self.url_queue.put(l)
            except Exception as e:
                return self.rentpost()
        print('28hse- 租盘已爬取完成！')

    def salepost(self):
        url = r'https://www.28hse.com/utf8/search3_ajax.php'
        while not self.sale_queue.empty():
            p=self.sale_queue.get()
            print('28hse-正在爬取最新售盘链接',p)
            formdata = {
                "the_alldata": "s_order=0&s_order_direction=0&s_type=0&s_sellrent=1&s_sellrange=0&s_sellrange_l=0&s_sellrange_h=0&s_rentrange=0&s_rentrange_l=0&s_rentrange_h=0&s_source=2&s_roomno=0&s_area=0&s_area_l=0&s_area_h=0&s_cached_fav=0&s_stored_fav=0&s_page=%s&s_myrelated=0&s_cat_child=0&s_restore_search_codition=0&s_global_tag=0&s_viewmode=0&s_age=0&s_age_l=0&s_age_h=0&s_rent=0&stypeg_1_mode=1&stypeg_1_18=1&stypeg_1_17=1&stypeg_1_10=1&stypeg_1_11=1&stypeg_1_5=1&stypeg_1_7=1&stypeg_1_6=1&stypeg_1_19=1&stypeg_8_16=0&s_keywords=&input_low=&input_high=&s_area_buildact=1&input_low=&input_high=&input_low=&input_high=" % p,
                "action": 200
            }
            data = urllib.parse.urlencode(formdata).encode(encoding='UTF-8')
            try:
                response = requests.session().post(url, data=data, headers=self.headers)
                link = re.findall(r'https://www.28hse.com/buy-property-\d+.html', response.text.replace("\/", "/"))
                link = list(set(link))
                for l in link:
                    self.url_queue.put(l)
            except Exception as e:
                return self.salepost()
        print('28hse-售盘已爬取完成！')



    def get_index(self,retires=1):
        while not self.url_queue.empty():
            url = self.url_queue.get()
            print('28hse-爬取', url)
            try:
                page = requests.session().get(url, headers=self.headers_)
            except Exception as e:
                if retires < 4:
                    print('28hse-链接超时，尝试重新链接第%s次' % retires)
                    time.sleep(2)
                    return self.get_index(retires + 1)
                else:
                    print('28hse-重连次数已达三次，请确认url正确或网络配置！\n当前url为', url)
            else:
                tree = html.fromstring(page.text)
                self.html_queue.put(tree)
                print(self.url_queue.qsize())
                self.url_queue.task_done()

    def extract_information(self):
        # url=r'https://www.28hse.com/rent-property-806377.html'
        # url=r'https://www.28hse.com/buy-property-830891.html'
        # page = requests.session().get(url, headers=self.headers_)
        # tree = html.fromstring(page.text)
        while not self.html_queue.empty():
            tree=self.html_queue.get()
            tex_fortel = tree.xpath('//ul[@class="clearfix"]/li[2]/dl/dt/b/text()')
            print(tex_fortel,self.html_queue.qsize())
            if tex_fortel != ['業主自讓盤']:
                pass
            com=tree.xpath('//div[@class="paid_agent_name obv"]/a/@href')
            if len(com)>0:
                lins = com[0]
                print(lins,self.html_queue.qsize())
                self.linss.append(lins)
                # df=pd.DataFrame({'links':self.linss})
                # df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse-公司网址.xlsx')
            else:
                uncn = re.compile(r'[\u0061-\u007a,\u0020]')
                chin = re.compile(r'[\u4e00-\u9fa5,\u0020]')
                tel_ = tree.xpath('//div[@class="agents_div"]//div/ul/li[2]/dl/dd//div/text()')
                name_ = tree.xpath('//div[@class="agents_div"]//div/ul/li[2]/dl//dd[1]/text()')
                tel1= tel_[0] if len(tel_)>0 else None
                tel1= re.findall(r'\d+',tel1.replace(" ","")) if tel1 is not None else None
                tel2= tel_[1] if len(tel_)>1 else None
                tel2 = re.findall(r'\d+', tel2.replace(" ", "")) if tel2 is not None else None
                tel3= tel_[2] if len(tel_)>2 else None
                tel3 = re.findall(r'\d+', tel3.replace(" ", "")) if tel3 is not None else None
                name1= name_[0] if len(name_)>0 else None
                chiname1="".join(chin.findall(name1.lower())) if name1 is not None else None
                engname1="".join(uncn.findall(name1.lower())) if name1 is not None else None
                name2= name_[1] if len(name_)>1 else None
                chiname2 = "".join(chin.findall(name2.lower())) if name2 is not None else None
                engname2 = "".join(uncn.findall(name2.lower())) if name2 is not None else None
                name3= name_[2] if len(name_)>2 else None
                chiname3 = "".join(chin.findall(name3.lower())) if name3 is not None else None
                engname3 = "".join(uncn.findall(name3.lower())) if name3 is not None else None
                com_ = tree.xpath('//div[@class="agents_div"]//div/ul/li[2]/dl//dd[2]/text()')
                com=com_[0] if len(com_)>0 else None
                item=[chiname1,engname1,tel1,chiname2,engname2,tel2,chiname3,engname3,tel3,com]
                self.information.append(item)
                # df=pd.DataFrame(self.information,columns=['中文名1','英文名1','电话1','中文名2','英文名2','电话2','中文名3','英文名3','电话3','所属公司'])
                # df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse-经纪人.xlsx')
                print(item,self.html_queue.qsize())
            self.html_queue.task_done()
        df1 = pd.DataFrame({'links': self.linss})
        df1.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse-公司网址.xlsx',index=None)
        df = pd.DataFrame(self.information,
                          columns=['中文名1', '英文名1', '电话1', '中文名2', '英文名2', '电话2', '中文名3', '英文名3', '电话3', '所属公司'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse-经纪人.xlsx',index=None)

    def ex_index(self,url):
        url=url[0]
        global G
        G+=1
        columns = ['中文名', '英文名', '電話1', '電話2', '代理牌照', '所屬公司', '分行地址']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        try:
            response = requests.session().get(url, headers=headers)
        except Exception as e:
            print('re downing')
            return self.ex_index(url)
        tree = html.fromstring(response.text)
        chinames = tree.xpath('//div[@class="agent_users_list"]//div/ul/li[2]/div/p[1]/text()')
        engnames = tree.xpath('//div[@class="agent_users_list"]//div/ul/li[2]/div/p[2]/text()')
        tel1s = tree.xpath('//div[@class="agent_users_list"]//div/ul/li[2]/div/p[3]/text()')
        tel2s = tree.xpath('//div[@class="agent_users_list"]//div/ul/li[2]/div/p[4]/text()')
        cards = tree.xpath('//div[@class="agent_users_list"]//div/ul/li[2]/div/p[5]/text()')
        com = tree.xpath('//div[@class="agent3_company"]/h2/a/text()')
        com = com[0] if len(com)>0 else None
        adress = tree.xpath('//table[@class="agent_info_t1"]/tr[4]/td/div/text()')
        adress = adress[0].replace("\n", "").replace(" ", "") if len(adress) > 0 else None
        print(G, url)
        for i in range(0, len(cards)):
            chiname = chinames[i] if len(chinames) > i else None
            engname = engnames[i] if len(engnames) > i else None
            tel1 = tel1s[i] if len(tel1s) > i else None
            tel2 = tel2s[i] if len(tel2s) > i else None
            card = cards[i] if len(cards) > i else None
            item = [chiname, engname, tel2, tel1, card, com, adress]
            self.items.append(item)
            print(item)
        df=pd.DataFrame(self.items,columns=columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse.xlsx',index=None)
    def run(self):
        thread_list = []
        postlist=[]
        self.page()
        for i in range(10):
            thread_parse1 = threading.Thread(target=self.rentpost)
            thread_parse2 = threading.Thread(target=self.salepost)
            postlist.append(thread_parse1)
            postlist.append(thread_parse2)
        for t in postlist:
            t.setDaemon(True)
            t.start()
        for t in postlist:
            t.join()
        for i in range(10):
            thread_parse = threading.Thread(target=self.get_index)
            thread_list.append(thread_parse)
        for t in thread_list:
            t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join()
        print(self.html_queue.qsize())
        self.extract_information()
        self.url_queue.join()
        self.html_queue.join()

    # def ex_index(self):

if __name__ == '__main__':

    hse=Hse28()
    urls = pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\28hse-公司网址.xlsx').values.tolist()
    G = 0
    for url in urls:
        hse.ex_index(url)

