import urllib
from queue import Queue
import re
import time
import threading
from bs4 import BeautifulSoup
import mysql.connector
import pandas as pd
import requests
from fake_useragent import UserAgent
class Spider():
    def __init__(self):
        self.ip = open(r'D:/ip', 'r').read()
        self.ua=UserAgent()
        self.sale_headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host': 'sale.591.com.hk',
                'Referer': 'https://sale.591.com.hk/',
                'User-Agent': '%s'%self.ua.chrome,
                'X-Requested-With': 'XMLHttpRequest'
            }#用于售盘POST
        self.rent_headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Connection':'keep-alive',
                'Host':'rent.591.com.hk',
                'Referer': 'https://rent.591.com.hk/',
                'User-Agent': '%s'%self.ua.chrome,
                'X-Requested-With':'XMLHttpRequest'
            }#用于租盘POST
        self.html_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        self.post_sale = r'https://sale.591.com.hk/?m=home&c=search&a=rslist&v=new&type=2&region=6&hasimg=1&shType=host&searchtype=1&p=1&role='
        self.post_rent = r'https://rent.591.com.hk/?m=home&c=search&a=rslist&v=new&type=1&region=6&hasimg=1&shType=host&searchtype=1&p=1&role='
        self.dic = {
            '堅尼地城': '堅尼地城/西營盤',
            '西營盤': '堅尼地城/西營盤',
            '西半山': '西半山',
            '金鐘': '中上環/金鐘',
            '中環': '中上環/金鐘',
            '上環': '中上環/金鐘',
            '山頂': '山頂',
            '灣仔': '灣仔/銅鑼灣',
            '銅鑼灣': '灣仔/銅鑼灣',
            '中半山': '中半山',
            '天后': '北角/炮台山/天后/大坑',
            '大坑': '北角/炮台山/天后/大坑',
            '北角': '北角/炮台山/天后/大坑',
            '炮台山': '北角/炮台山/天后/大坑',
            '北角半山': '北角半山',
            '大坑道': '跑馬地/東半山',
            '跑馬地': '跑馬地/東半山',
            '司徒拔道': '跑馬地/東半山',
            '樂活道': '跑馬地/東半山',
            '渣甸山': '跑馬地/東半山',
            '鰂魚涌': '鰂魚涌',
            '西灣河': '鰂魚涌',
            '筲箕灣': '筲箕灣',
            '太古城': '太古城',
            '柴灣': '柴灣/小西灣',
            '小西灣': '柴灣/小西灣',
            '藍灣半島': '柴灣/小西灣',
            '杏花村': '杏花村',
            '薄扶林': '薄扶林',
            '碧瑤灣': '薄扶林',
            '置富': '薄扶林',
            '碧麗道': '薄扶林',
            '赤柱': '赤柱/大潭',
            '大潭': '赤柱/大潭',
            '石澳': '赤柱/大潭',
            '舂磡角': '赤柱/大潭',
            '深水灣': '深水灣/淺水灣/壽臣山道',
            '壽臣山': '深水灣/淺水灣/壽臣山道',
            '淺水灣': '深水灣/淺水灣/壽臣山道',
            '貝沙灣': '貝沙灣',
            '海怡半島': '鴨脷洲',
            '鴨脷洲': '鴨脷洲',
            '深灣軒': '鴨脷洲',
            '南灣': '鴨脷洲',
            '黃竹坑': '香港仔/田灣/黃竹坑',
            '香港仔': '香港仔/田灣/黃竹坑',
            '田灣': '香港仔/田灣/黃竹坑',
            '深水埗': '深水埗/長沙灣',
            '長沙灣': '深水埗/長沙灣',
            '荔枝角': '深水埗/長沙灣',
            '長沙灣西': '長沙灣西',
            '旺角': '旺角/太子',
            '太子': '旺角/太子',
            '美孚': '美孚/華景',
            '油麻地': '佐敦/油麻地',
            '佐敦': '佐敦/油麻地',
            '尖沙咀': '尖沙咀/九龍站',
            '九龍站': '尖沙咀/九龍站',
            '奧運站': '奧運/大角咀',
            '大角咀': '奧運/大角咀',
            '南昌': '奧運/大角咀',
            '寶琳': '將軍澳',
            '調景嶺': '將軍澳',
            '將軍澳': '將軍澳',
            '坑口': '將軍澳',
            '日出康城': '日出康城',
            '石硤尾': '又一村/石硤尾',
            '九龍塘': '九龍塘/畢架山',
            '何文田': '何文田/京士柏',
            '京士柏': '何文田/京士柏',
            '藍田': '藍田/油塘',
            '油塘': '藍田/油塘',
            '九龍灣': '九龍灣',
            '牛頭角': '九龍灣',
            '啟德': '新蒲崗/啟德',
            '新蒲崗': '新蒲崗/啟德',
            '觀塘': '觀塘',
            '秀茂坪': '觀塘',
            '黃大仙': '九龍城/鑽石山',
            '樂富': '九龍城/鑽石山',
            '鑽石山': '九龍城/鑽石山',
            '九龍城': '九龍城/鑽石山',
            '彩虹': '九龍城/鑽石山',
            '土瓜灣': '土瓜灣',
            '紅磡': '紅磡/黃埔',
            '黃埔': '紅磡/黃埔',
            '汀角路': '大埔半山/康樂園',
            '康樂園': '大埔半山/康樂園',
            '大埔半山': '大埔半山/康樂園',
            '大埔墟': '大埔墟/太和',
            '太和': '大埔墟/太和',
            '粉嶺': '上水/粉嶺/古洞',
            '上水': '上水/粉嶺/古洞',
            '清水灣': '西貢',
            '飛鵝山': '西貢',
            '白沙灣': '西貢',
            '蠔涌/匡湖居': '西貢',
            '西貢市': '西貢',
            '西沙路': '西貢',
            '銀線灣': '西貢',
            '大網仔': '西貢',
            '大圍': '大圍',
            '大圍半山': '大圍',
            '沙田': '沙田',
            '火炭': '火炭/沙田半山/九肚山',
            '沙田半山': '火炭/沙田半山/九肚山',
            '九肚山': '火炭/沙田半山/九肚山',
            '馬鞍山': '馬鞍山',
            '愉景灣': '愉景灣',
            '屏山': '新田/十八鄉/大棠',
            '大棠': '新田/十八鄉/大棠',
            '新田': '新田/十八鄉/大棠',
            '十八鄉': '新田/十八鄉/大棠',
            '元朗': '元朗市中心/洪水橋/錦上路',
            '洪水橋': '元朗市中心/洪水橋/錦上路',
            '錦上路': '元朗市中心/洪水橋/錦上路',
            '屯門': '屯門',
            '藍地': '屯門',
            '龍鼓灘': '屯門',
            '深井（屯門）': '青山公路(屯門段)',
            '嘉湖山莊': '天水圍',
            '天水圍': '天水圍',
            '荃灣': '荃灣',
            '大窩口': '荃灣',
            '深井（荃灣）': '麗城/青山公路(荃灣段)',
            '青衣': '葵涌/青衣/馬灣',
            '馬灣': '葵涌/青衣/馬灣',
            '葵涌': '葵涌/青衣/馬灣',
            '大嶼山': '東涌/離島',
            '坪洲': '東涌/離島',
            '長洲': '東涌/離島',
            '南丫島': '東涌/離島',
            '大澳': '東涌/離島',
            '其他離島': '東涌/離島',
            '東涌': '東涌/離島'
        }
        self.dic2 ={
            '鰂魚涌': '鰂魚涌', '太古/西灣河': '西灣河', '筲箕灣': '筲箕灣', '柴灣': '柴灣', '壽臣山': '壽臣山', '淺水灣': '淺水灣', '赤柱/大潭': '赤柱',
         '南區/石澳': '石澳', '香港仔': '香港仔', '薄扶林/海怡': '薄扶林', '貝沙灣': '貝沙灣', '西半山': '西半山', '西區': '西半山', '上環/中環': '上環',
         '中半山/金鐘': '中半山', '灣仔': '灣仔', '銅鑼灣': '銅鑼灣', '跑馬地': '跑馬地', '天后/大坑': '天后', '北角': '北角', '山頂': '山頂', '油塘/藍田': '油塘',
         '觀塘/秀茂坪': '觀塘', '九龍灣': '九龍灣', '鑽石山/彩虹': '鑽石山', '康城/清水灣': '清水灣', '九龍城': '九龍城', '土瓜灣': '土瓜灣', '佐敦/尖沙咀': '佐敦',
         '九龍站': '九龍站', '紅磡/黃埔': '紅磡', '深水埗': '深水埗', '長沙灣': '長沙灣', '荔枝角': '荔枝角', '啟德': '啟德', '美孚': '美孚', '大角咀': '大角咀',
         '奧運': '奧運站', '九龍塘': '九龍塘', '石硤尾': '石硤尾', '何文田/京士柏': '何文田', '黃大仙/新蒲崗': '黃大仙', '太子': '太子', '旺角/油麻地': '旺角',
         '西貢': '西貢市', '馬鞍山': '馬鞍山', '大埔/太和': '太和', '將軍澳': '將軍澳', '沙田/火炭': '沙田', '深井': '深井（屯門）', '荃灣': '荃灣', '葵涌': '葵涌',
         '青衣': '青衣', '元朗': '元朗', '天水圍': '天水圍', '屯門': '屯門', '粉嶺': '粉嶺', '上水': '上水', '調景嶺': '調景嶺', '大窩口': '大窩口',
         '愉景灣': '愉景灣', '東涌': '東涌', '馬灣': '馬灣', '大嶼山': '大嶼山', '坪洲': '坪洲', '南丫島': '南丫島', '長洲': '長洲', '離島': '其他離島'
        }
        self.rentpage_queue = Queue() #页码
        self.salepage_queue = Queue()
        self.url_queue = Queue()  # 实例化三个队列，用来存放内容
        self.html_queue = Queue()
        self.index_queue = Queue()

    def get_page(self):#获取页面数
        salepages=[]
        try:
            req = requests.session().get(self.post_sale, headers=self.sale_headers,timeout=5)
        except Exception as e:
            time.sleep(2)
            return self.get_page()
        text = req.text.replace("\/", "/")
        page = re.findall(r'data-page=(\d+)', text)
        for salepage in page:
            salepages.append(int(salepage))
        try:
            salepage = max(salepages)
        except Exception as e:
            time.sleep(2)
            return self.get_page()
        print('售盘%s页'%salepage)
        for a in range(1,salepage+1):
            self.salepage_queue.put(a)
        rentpages=[]
        try:
            req = requests.session().get(self.post_rent, headers=self.rent_headers,timeout=5)
        except Exception as e:
            time.sleep(2)
            return self.get_page()
        text = req.text.replace("\/", "/")
        page = re.findall(r'data-page=(\d+)', text)
        for rentpage in page:
            rentpages.append(int(rentpage))
        try:
            rentpage = max(rentpages)
        except Exception as e:
            time.sleep(2)
            return self.get_page()
        print('租盘%s页'%rentpage)
        for b in range(1,rentpage+1):
            self.rentpage_queue.put(b)

    def salepost(self):
        while not self.salepage_queue.empty():
            salepage=self.salepage_queue.get()
            self.salepage_queue.task_done()
            self._salepost_(salepage)
            time.sleep(2)


    def rentpost(self):
        while not self.rentpage_queue.empty():
            rentpage = self.rentpage_queue.get()
            self.rentpage_queue.task_done()
            self._rentpost_(rentpage)
            time.sleep(2)

    def _salepost_(self,salepage):
        print('591-正在爬取售盘第%s页' % salepage)
        number = []
        conn = mysql.connector.connect(host=self.ip, user='spider', password='123456', database='spider')
        t3 = time.strftime("%Y-%m-%d", time.localtime())
        cursor = conn.cursor()
        cursor.execute('DELETE FROM spider591 WHERE datediff(curdate(), days)>=14')
        conn.commit()  # 删除旧编号
        cursor.execute('select * from spider591')
        values = cursor.fetchall()
        for v in values:
            number.append(v[0])
        surl = r'https://sale.591.com.hk/?m=home&c=search&a=rslist&v=new&type=2&region=6&hasimg=1&shType=host&searchtype=1&p=%s&role=' % salepage
        try:
            req = requests.session().get(surl, headers=self.sale_headers, timeout=5)
        except Exception as e:
            print('591-售盤第%s頁鏈接超重連' % salepage)
            time.sleep(2)
            return self._salepost_(salepage)
        text = req.text.replace("\/", "/")
        links = re.findall(r'https://sale.591.com.hk/sale-detail-\d+.html\?z=[0-9\_]+', text)
        for link in links:
            num = int(re.findall(u'(\d+).html', link)[0])
            if num not in number:
                self.url_queue.put(link)
                cursor.execute('INSERT into spider591 VALUES(%s,"%s")' % (num, t3))
                conn.commit()
        cursor.close()
        conn.close()


    def _rentpost_(self,rentpage):
        print('591-正在爬取租盘第%s页' % rentpage)
        number = []
        conn = mysql.connector.connect(host=self.ip, user='spider', password='123456', database='spider')
        t3 = time.strftime("%Y-%m-%d", time.localtime())
        cursor = conn.cursor()
        cursor.execute('DELETE FROM spider591 WHERE datediff(curdate(), days)>=14')
        conn.commit()  # 删除旧编号
        cursor.execute('select * from spider591')
        values = cursor.fetchall()
        for v in values:
            number.append(v[0])
        rurl = r'https://rent.591.com.hk/?m=home&c=search&a=rslist&v=new&type=1&region=6&hasimg=1&shType=host&searchtype=1&p=%s&role=' % rentpage
        try:
            req = requests.session().get(rurl, headers=self.rent_headers, timeout=5)
        except Exception as e:
            print('591-租盤第%s頁鏈接超時重連' % rentpage)
            time.sleep(2)
            return self._rentpost_(rentpage)
        text = req.text.replace("\/", "/")
        links = re.findall(r'https://rent.591.com.hk/rent-detail-\d+.html\?z=[0-9\_]+', text)
        for link in links:
            num = int(re.findall(u'(\d+).html', link)[0])
            if num not in number:
                self.url_queue.put(link)
                cursor.execute('INSERT into spider591 VALUES(%s,"%s")' % (num, t3))
                conn.commit()
        cursor.close()
        conn.close()

    def get_html(self):
        while not self.url_queue.empty():
            url=self.url_queue.get()
            self.url_queue.task_done()
            self._get_html_(url)


    def _get_html_(self,url,reget=1):
        print('591--爬取', url)
        try:
            req = urllib.request.Request(url=url, headers=self.html_headers)
            content = urllib.request.urlopen(req, timeout=50).read()
        except Exception as e:
            if reget < 4:
                print('591-链接出现错误或者超时,将在10S后进行第%s次重试' % reget)
                time.sleep(10)
                return self._get_html_(url, reget=reget + 1)
            else:
                print('591-请检查网络！')
        else:
            soup = BeautifulSoup(content, 'html.parser')
            self.html_queue.put(soup)

    def get_index(self):
        while not self.html_queue.empty():
            items = []
            soup=self.html_queue.get()
            # ----------判断租售---------
            status=soup.find(class_='bread-nav-item',recursive=True).get_text().split()[1]
            if '租' in status:
                statu='租'
            else:
                statu='售'
            # ----------区域地址---------
            adress_ = soup.find('em', text='地址', recursive=True).parent.p.get_text().strip().split(' ', 1)
            loc = re.findall(u'[\-].*', adress_[0])[0].replace('-', '')
            if len(adress_) > 1:
                adress = adress_[1].strip()
            else:
                adress = ''
            # ----------改写区域地段---------
            loca=self.dic2.get(loc)
            region=self.dic.get(loca)
            # ----------物业名称------------
            property = soup.find('em', text='物業', recursive=True)
            if property is None:
                property = adress
            else:
                property = property.parent.p.get_text()
            propertys = property.strip()
            # -----------樓層---------------
            floor_ = soup.find('em', text='樓層：', recursive=True)
            if floor_ is None:
                floor = ''
            else:
                if '/' in floor_.parent.get_text():
                    floor = re.findall(u'[\u4E00-\u9FA5,/d]*[/]', floor_.parent.get_text())[0].replace('/', '')
                else:
                    floor = re.findall(u'\d+', floor_.parent.get_text())[0]
            # -----------價格---------------
            price1 = soup.find(id='price', recursive=True).get_text()
            if statu == '租':
                rent = price1.replace(",", "")
                price = ''
            if statu == '售':
                price = price1.replace(",", "")
                rent = ''
            # -----------面積---------------
            pb_area = soup.find('em', text='面積', recursive=True)
            if pb_area is None:
                scantling = ''
                actual_size = ''
            else:
                pb_area = pb_area.next_sibling.get_text()
                area = re.findall(u'[\d]+呎', pb_area)
                if len(area) == 1:
                    if '建' in pb_area:
                        area.insert(0, '')
                    else:
                        area.insert(1, '')
                scantling = area[1].replace("呎", "")
                actual_size = area[0].replace("呎", "")
            # -----------間隔---------------
            interval_ = soup.find('em', text='間隔', recursive=True)
            if interval_ is None:
                interval = ''
            else:
                interval = interval_.next_sibling.get_text()
            # -----------用途---------------
            usage_ = soup.find(id='use-type', recursive=True).get_text()
            usage_ = usage_.replace("工廠大廈", "工廈")
            if '-' in usage_:
                usage = re.findall(u'.*[-]', usage_)[0].replace('-', '')
            else:
                usage = re.findall(u'[\u4E00-\u9FA5]*', usage_)[0]
            # -----------聯繫人與電話---------------
            name = soup.find(class_='name', recursive=True).get_text().replace('(業主)', '').strip()
            tel_ = soup.find(class_='new-tel', recursive=True)
            if tel_ is None:
                tel = ''
            else:
                tel = tel_.get_text().strip().replace(' ', '')
            # -----------編號--------------
            id = soup.find('span', text='>', recursive=True).parent.get_text().split()[-1]
            ids = re.findall(u'\d+', id)[0]
            # -----------其他--------------
            character = '業主'
            source = '591'
            t1 = time.strftime('%d/%m/20%y', time.localtime(time.time()))
            item = dict(
                日期=t1,
                來源=source,
                租售=statu,
                租金=rent,
                售價=price,
                實呎=actual_size,
                建呎=scantling,
                區域=region,
                地段=loca,
                街道=adress,
                物業名稱=propertys,
                期=None,
                座=None,
                樓層=floor,
                室號=None,
                車位號碼=None,
                備註=None,
                聯絡人1=name,
                電話1=tel,
                聯絡人2=None,
                電話2=None,
                聯絡人3=None,
                電話3=None,
                單位類別=usage,
                聯絡人性質=character,
                佣金=None,
                編號=ids,
                間隔=interval
            )
            items.append(item)
            self.index_queue.put(items)
            self.html_queue.task_done()

    def save_items(self):
        information=[]
        columns = ['日期', '來源', '租售', '租金', '售價', '實呎', '建呎', '區域', '地段', '街道', '物業名稱', '期', '座', '樓層',
                   '室號', '車位號碼', '備註', '聯絡人1', '電話1', '聯絡人2', '電話2', '聯絡人3', '電話3', '單位類別', '聯絡人性質',
                   '佣金', '編號', '間隔']
        t=time.strftime('%m-%d', time.localtime(time.time()))
        while not self.index_queue.empty():
            items=self.index_queue.get()[0]
            information.append(list(items.values()))
            self.index_queue.task_done()
        df=pd.DataFrame(information,columns=columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\jianbao\每日\591-%s.xlsx' % t, index=None)

    def run(self):
        self.get_page()
        thread_list=[]
        post_list=[]
        for i in range(10):
            thread_rentpost=threading.Thread(target=self.rentpost)
            thread_salepost = threading.Thread(target=self.salepost)
            post_list.append(thread_rentpost)
            post_list.append(thread_salepost)
        for t in post_list:
            # t.setDaemon(True)
            t.start()
        for t in post_list:
            t.join(60)
        for i in range(10):
            thread_parse=threading.Thread(target=self.get_html)
            thread_list.append(thread_parse)
        for t in thread_list:
            # t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join(300)
        self.get_index()
        self.save_items()
        self.url_queue.join()
        self.html_queue.join()
        self.index_queue.join()


if __name__ == '__main__':
    sp591 = Spider()
    starttime = time.time()
    sp591.run()
    end = time.time()
    print('591-爬取完成，共耗時', (end - starttime))