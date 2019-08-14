from queue import Queue
import urllib
import requests
import re
import time
import pandas as pd
from lxml import html
import threading
import mysql.connector
from dateutil.parser import parse
class Hse28:
    def __init__(self,rentpage,salepage):
        self.information=[]
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
                   'Accept': 'application/json, text/javascript, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest',
                   'Origin': 'https://www.28hse.com', 'Referer': 'https://www.28hse.com/buy',
                   'Content-Type': 'application/x-www-form-urlencoded'}#用于发送POST请求
        self.headers_= {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}#用于获取页面信息
        self.usedict={
            "商務中心": "寫字樓",
            "工商": "工廈",
            "店舖": "商舖",
            "農地或倉地": "土地",
            "服務式住宅":"住宅"
        }#用途字典
        self.dic={
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
        self.dic2={
            '西營盤': '西營盤',
            '石塘咀': '西營盤',
            '堅尼地城': '堅尼地城',
            '上環': '上環',
            '中環': '中環',
            '西半山': '西半山',
            '中半山': '中半山',
            '山頂': '山頂',
            '金鐘': '金鐘',
            '灣仔': '灣仔',
            '肇輝臺': '灣仔',
            '跑馬地': '跑馬地',
            '跑馬地半山': '跑馬地',
            '銅鑼灣': '銅鑼灣',
            '大坑': '大坑',
            '天后': '天后',
            '渣甸山': '渣甸山',
            '北角': '北角',
            '北角半山': '北角半山',
            '炮台山': '炮台山',
            '鰂魚涌': '鰂魚涌',
            '太古城': '太古城',
            '西灣河': '西灣河',
            '筲箕灣': '筲箕灣',
            '杏花村': '杏花村',
            '柴灣': '柴灣',
            '石澳': '石澳',
            '黃竹坑': '黃竹坑',
            '香港仔': '香港仔',
            '鴨脷洲': '鴨脷洲',
            '薄扶林': '薄扶林',
            '壽臣山': '壽臣山',
            '碧瑤灣': '碧瑤灣',
            '南區': '淺水灣',
            '淺水灣': '淺水灣',
            '大潭': '大潭',
            '赤柱': '赤柱',
            '海怡半島': '海怡半島',
            '楊明山莊': '大潭',
            '油塘': '油塘',
            '藍田': '藍田',
            '觀塘': '觀塘',
            '牛頭角': '牛頭角',
            '牛池灣': '彩虹',
            '九龍灣': '九龍灣',
            '樂富': '樂富',
            '鑽石山': '鑽石山',
            '啟德': '啟德',
            '土瓜灣': '土瓜灣',
            '九龍城': '九龍城',
            '新蒲崗': '新蒲崗',
            '黃大仙': '黃大仙',
            '九龍塘': '九龍塘',
            '何文田': '何文田',
            '又一村': '石硤尾',
            '石硤尾': '石硤尾',
            '深水埗': '深水埗',
            '荔枝角': '荔枝角',
            '長沙灣': '長沙灣西',
            '美孚': '美孚',
            '荔景': '荔枝角',
            '大角咀': '大角咀',
            '奧運': '奧運站',
            '九龍站': '九龍站',
            '太子': '太子',
            '旺角': '旺角',
            '油麻地': '油麻地',
            '尖沙咀': '尖沙咀',
            '佐敦': '佐敦',
            '紅磡': '紅磡',
            '黃埔': '黃埔',
            '西貢': '西貢市',
            '清水灣': '清水灣',
            '將軍澳': '將軍澳',
            '馬鞍山': '馬鞍山',
            '沙田': '沙田',
            '大圍': '大圍',
            '火炭': '火炭',
            '大埔': '大埔墟',
            '太和': '太和',
            '粉嶺': '粉嶺',
            '上水': '上水',
            '元朗': '元朗',
            '天水圍': '天水圍',
            '屯門': '深井（屯門）',
            '深井(屯門)': '深井（屯門）',
            '深井(荃灣)': '深井（荃灣）',
            '荃灣': '荃灣',
            '大窩口': '大窩口',
            '葵涌': '葵涌',
            '葵芳': '葵涌',
            '青衣': '青衣',
            '馬灣': '馬灣',
            '愉景灣': '愉景灣',
            '東涌': '東涌',
            '南大嶼山': '大嶼山',
            '坪洲': '坪洲',
            '大澳': '大澳',
            '南丫島': '南丫島',
            '長洲': '長洲',
            '其他離島': '其他離島'
        }
        self.ip=open(r'D:/ip','r').read()#数据库的ip地址，用于查重等操作
        self.rentpage=rentpage
        self.salepage=salepage#(需要爬取的页数，通常租盘12，售盘5，周一翻倍)
        self.url_queue = Queue()# 实例化三个队列，用来存放内容 （Queue：用于进程间通信的容器）
        self.html_queue = Queue()
        self.index_queue = Queue()

    def input_page(self):#手动输入页码，目前已弃用
        trs = input('请输入序号：\n1.爬取默认页数(租盘12页、售盘5页)\n2.自行输入爬取页数\n————')
        if trs == '1':
            rentpage = 12
            salepage = 5
            print('租盘%s页，售盘%s页' % (rentpage, salepage))
        elif trs == '2':
            rentpage = input('请输入租盘页数：')
            salepage = input('请输入售盘页数：')
            try:
                rentpage = int(rentpage)
                salepage = int(salepage)
            except ValueError as e:
                print('输入错误,请输入纯数字！')
                return input_page()
            print('租盘%s页，售盘%s页' % (rentpage, salepage))
        else:
            print('输入错误，请重新输入')
            return self.input_page()
        return rentpage, salepage

    def post(self):
        number=[]
        t3 = time.strftime("%Y-%m-%d", time.localtime())#读取今天时间
        conn = mysql.connector.connect(host=self.ip,user='spider', password='123456', database='spider')#连接数据库
        cursor = conn.cursor()
        cursor.execute('DELETE FROM hse28 WHERE datediff(curdate(), days)>=14')#删除旧编号
        conn.commit()#提交
        cursor.execute('select * from hse28')#查询
        values = cursor.fetchall()
        for v in values:
            number.append(v[0])#将查询出来的编号放入一个list中
        url = r'https://www.28hse.com/utf8/search3_ajax.php'#28hse查询二手盘的请求url
        for i in [1, 2]:  # 1是售 2是租
            if i == 1:
                print('28hse-正在爬取最新售盘链接')
                for p in range(1, self.salepage + 1):
                    formdata = {
                        "the_alldata": "s_order=1&s_order_direction=0&s_type=0&s_sellrent=1&s_sellrange=0&s_sellrange_l=0&s_sellrange_h=0&s_rentrange=0&s_rentrange_l=0&s_rentrange_h=0&s_source=1&s_roomno=0&s_area=0&s_area_l=0&s_area_h=0&s_cached_fav=0&s_stored_fav=0&s_page=%s&s_myrelated=0&s_cat_child=0&s_restore_search_codition=0&s_global_tag=0&s_viewmode=0&s_age=0&s_age_l=0&s_age_h=0&s_rent=0&stypeg_1_mode=1&stypeg_1_18=1&stypeg_1_17=1&stypeg_1_10=1&stypeg_1_11=1&stypeg_1_5=1&stypeg_1_7=1&stypeg_1_6=1&stypeg_1_19=1&stypeg_8_16=0&s_keywords=&input_low=&input_high=&s_area_buildact=1&input_low=&input_high=&input_low=&input_high=" % p,
                        "action": 200
                    }#查询售盘用的data 可在network里查到
                    data = urllib.parse.urlencode(formdata).encode(encoding='UTF-8')#将data进行解码
                    response = requests.session().post(url, data=data, headers=self.headers)#发送post请求，注意是post不是get，并加入data和headers
                    link = re.findall(r'https://www.28hse.com/buy-property-\d+.html', response.text.replace("\/", "/"))#正则表达式提取二手盘链接
                    link = list(set(link))#将提取到的链接去重
                    for l in link:
                        num = str(re.findall(u'(\d+).html',l)[0])
                        if num not in number:#编号14天去重
                            self.url_queue.put(l)#url_queue中加入需要爬取的url
                            cursor.execute('INSERT into hse28 VALUES(%s,"%s")' % (num, t3))#加入新编号和当天日期
                            conn.commit()#提交
                print('28hse-售盘已爬取完成！')
            else:
                print('28hse-正在爬取最新租盘链接')
                for p in range(1, self.rentpage + 1):
                    formdata = {
                        "the_alldata": "s_order=1&s_order_direction=0&s_type=0&s_sellrent=2&s_sellrange=0&s_sellrange_l=0&s_sellrange_h=0&s_rentrange=0&s_rentrange_l=0&s_rentrange_h=0&s_source=1&s_roomno=0&s_area=0&s_area_l=0&s_area_h=0&s_cached_fav=0&s_stored_fav=0&s_page=%s&s_myrelated=0&s_cat_child=0&s_restore_search_codition=0&s_global_tag=0&s_viewmode=0&s_age=0&s_age_l=0&s_age_h=0&s_rent=0&stypeg_1_mode=1&stypeg_1_18=1&stypeg_1_17=1&stypeg_1_10=1&stypeg_1_11=1&stypeg_1_5=1&stypeg_1_7=1&stypeg_1_6=1&stypeg_1_19=1&stypeg_8_16=0&s_keywords=&input_low=&input_high=&s_area_buildact=1&input_low=&input_high=&input_low=&input_high=" % p,
                        "action": 200
                    }
                    data = urllib.parse.urlencode(formdata).encode(encoding='UTF-8')
                    response = requests.session().post(url, data=data, headers=self.headers)
                    link = re.findall(r'https://www.28hse.com/rent-property-\d+.html', response.text.replace("\/", "/"))
                    link = list(set(link))
                    for l in link:
                        num = re.findall(u'(\d+).html',l)[0]
                        num = str(num)
                        if num not in number:
                            self.url_queue.put(l)
                            cursor.execute('INSERT into hse28 VALUES(%s,"%s")' % (num, t3))
                            conn.commit()
                print('28hse- 租盘已爬取完成！')
                print('28hse- 已去重,剩余%s条' % self.url_queue.qsize())

        cursor.close()
        conn.close()

    def get_html(self,retires=1):#从url中提取源码出来
        while not self.url_queue.empty():#只要url_queue不为空，就无限重复下去
            url=self.url_queue.get()#在queue中拿一个url出来
            self.url_queue.task_done()#由于是10线程，为避免堵塞，拿出后马上表明这个url已经完成，其他线程不可再拿
            print('28hse-爬取',url)
            try:
                page=requests.session().get(url,headers=self.headers_)#获取网页源码
            except Exception as e:#网页超时重试
                if retires < 4:
                    print('28hse-链接超时，尝试重新链接第%s次' % retires)
                    time.sleep(2)
                    self.url_queue.put(url)#由于前面已经告知url完成，重试需要重新加入queue中
                    return self.get_html(retires + 1)
                else:
                    print('28hse-重连次数已达三次，请确认url正确或网络配置！\n当前url为', url)
            else:
                tree=html.fromstring(page.text)#转换结构
                self.html_queue.put(tree)#将转换后的源码加入html_queue中，待下一步爬取

    def extract_information(self):#从网页源码中提取数据
        while not self.html_queue.empty():#只要html_queue不为空，就无限重复下去
            source = '28hse'  # 來源
            nature = '業主'
            t1 = time.strftime('%d/%m/20%y', time.localtime(time.time()))
            items = []
            tree = self.html_queue.get()
            trs = tree.xpath('//table[@class="de_box_table"]//td/text()')  # 楼盘是否为空
            tex_fortel = tree.xpath('//ul[@class="clearfix"]/li[2]/dl/dt/b/text()')  # 楼盘性质是否符合条件
            tex_fortel_ = tree.xpath('//ul[@class="clearfix"]/li[2]/dl/dd[3]/text()')  # 电话是否符合条件
            if trs == []:
                print('28hse- 无楼盘信息')
            elif tex_fortel != ['業主自讓盤']:
                print('28hse- 代理盘')
            elif tex_fortel_ == ['Tel:業主並沒有公開電話聯絡方法，請留言']:
                print('28hse- 業主並沒有公開電話聯絡方法')
            elif tex_fortel_ == ['Tel:隱藏已售/已租單位']:
                print('28hse- 已租/售出')
            elif tex_fortel_ == ['Tel:因為放盤尚未付款，故聯絡方法不會顯示。聯絡方法會於樓盤付款後顯示出來。']:
                print('28hse- 楼盘未生效')
            elif tex_fortel_ == ['Tel:已封盤']:
                print('28hse- 已封盤')
            elif tex_fortel_ == ['Tel:樓盤進行審批中']:
                print('28hse- 樓盤進行審批中')
            else:  # 开始清洗
                number = tree.xpath('//table[@class="de_box_table"]//tr/th[text()="28HSE 樓盤編號"]/following-sibling::td[1]/text()')[0]#編號
                state=tree.xpath('//table[@class="de_box_table"]//tr/th[text()="樓盤狀態"]/following-sibling::td[1]/text()')[0].strip().replace("待","")#租售狀態
                if state == "售":
                    price_ = tree.xpath('//td[@valign="middle"]/div/text()')[0].replace(",","")#售價
                    price=re.findall(r'\d+',price_)[0]
                    rentmoney=None
                else:
                    rentmoney_=tree.xpath('//div[@class="green_numberic detail_large_fonts"]/text()')[0].replace(",","")#租價
                    rentmoney = re.findall(r'\d+', rentmoney_)[0]
                    price=None
                scantling_ = tree.xpath(
                    '//table[@class="de_box_table"]//tr/th[text()="建築面積(呎)"]/following-sibling::td[1]/text()')
                scantling=scantling_[0].replace(",","").strip() if len(scantling_)>0 else None
                actual_size_=tree.xpath(
                    '//table[@class="de_box_table"]//tr/th[text()="實用面積(呎)"]/following-sibling::td[1]/text()')
                actual_size=actual_size_[0].replace(",","").strip() if len(actual_size_)>0 else None
                loca_ = tree.xpath('//div[@class="feature_div_cat"]/span/text()')
                loca = self.dic2.get(loca_[0])
                region = self.dic.get(loca)
                propertys = loca_[1] if len(loca_)>1 else None
                stage=loca_[2] if len(loca_)>2 else None
                street = tree.xpath('//div[@class="map_add"]/text()')[0].strip()
                building_ = tree.xpath(
                    '//table[@class="de_box_table"]//tr/th[text()="座數及單位"]/following-sibling::td[1]/text()')
                building=building_[0] if len(building_)>0 else None
                jiange_ = tree.xpath(
                    '//table[@class="de_box_table"]//tr/th[text()="房間"]/following-sibling::td[1]/text()')
                jiange = jiange_[0].replace("+", "").strip() if len(jiange_) > 0 else None
                if jiange != '開放式' and jiange != None:
                    jiange += '房'
                floor_ = tree.xpath(
                    '//table[@class="de_box_table"]//tr/th[text()="層數"]/following-sibling::td[1]/text()')
                floor=floor_[0] if len(floor_)>0 else None
                name = tree.xpath('//ul[@class="clearfix"]/li[2]/dl/dd/text()')[0].strip()
                tel_ = tree.xpath('//div[@class="call_me_direct"]/div/text()')
                if tel_ == []:
                    tel=None
                else:
                    tel = re.findall(r'\d+',tel_[0].replace(" ",""))[0]
                use_ = tree.xpath('//div[@class="ad_type_style"]/span/text()')
                if len(use_)>1 and use_[1] == '工商':
                    us= tree.xpath('//div[@class="ad_type_style"]/span/text()')[1]
                else:
                    us=use_[0]
                use = self.usedict.get(us)#改写用途
                if use is None:
                    use = us
                print('28hse-',propertys,tel)
                item=dict(
                    日期 = t1,
                    來源 = source,
                    租售= state,
                    租金 = rentmoney,
                    售價 = price,
                    實呎 = actual_size,
                    建呎 = scantling,
                    區域 = region,
                    地段 = loca,
                    街道 = street,
                    物業名稱 = propertys,
                    期 = stage,
                    座 = building,
                    樓層 = floor,
                    室號 = None,
                    車位號碼 = None,
                    備註 = None,
                    聯絡人1 = name,
                    電話1 = tel,
                    聯絡人2 = None,
                    電話2 = None,
                    聯絡人3 = None,
                    電話3 = None,
                    單位類別 = use,
                    聯絡人性質 = nature,
                    佣金 = None,
                    編號 = number,
                    間隔 = jiange
                )
                items.append(item)
                self.index_queue.put(items)
            self.html_queue.task_done()

    def save_items(self):#储存数据
        while not self.index_queue.empty():#只要index_queue不为空，就无限重复下去
            items=self.index_queue.get()[0]
            columns = ['日期', '來源', '租售', '租金', '售價', '實呎', '建呎', '區域', '地段', '街道', '物業名稱', '期', '座', '樓層',
                       '室號', '車位號碼', '備註', '聯絡人1', '電話1', '聯絡人2', '電話2', '聯絡人3', '電話3', '單位類別', '聯絡人性質',
                       '佣金', '編號', '間隔']
            t = time.strftime('%m-%d', time.localtime(time.time()))
            self.information.append(list(items.values()))
            self.index_queue.task_done()
            df=pd.DataFrame(self.information,columns=columns)
            df.to_excel(r'C:\Users\Administrator\Desktop\jianbao\每日\28hse-%s.xlsx' % t, index=None)

    def run(self):#运行整个程序
        thread_list=[]
        self.post()
        for i in range(10):#10线程跑get_html
            thread_parse=threading.Thread(target=self.get_html)
            thread_list.append(thread_parse)
        for t in thread_list:
            # t.setDaemon(True)
            t.start()
        for t in thread_list:
            t.join(60)
        self.extract_information()
        self.save_items()
        self.url_queue.join()
        self.html_queue.join()
        self.index_queue.join()#待3个queue均为空方可结束程序



if __name__=='__main__':
    hse=Hse28(12,5)
    starttime=time.time()
    hse.run()
    end=time.time()
    print('28hse- 爬取完成，共耗時',(end-starttime))
