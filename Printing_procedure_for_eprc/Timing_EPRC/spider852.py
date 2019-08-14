from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
import time
import random
from queue import Queue
import threading
from decimal import Decimal
import mysql.connector

class eft:
    def __init__(self,page=7):
        self.ip = open(r'D:/ip', 'r').read()
        self.page=page
        self.pages=Queue()
        self.url=Queue()
        self.newnum=[]
        self.columns = [
            '日期',
            '來源',
            '租售',
            '租金',
            '售價',
            '實呎',
            '建呎',
            '區域',
            '地段',
            '街道',
            '物業名稱',
            '期',
            '座',
            '樓層',
            '室號',
            '車位號碼',
            '備註',
            '聯絡人1',
            '電話1',
            '聯絡人2',
            '電話2',
            '聯絡人3',
            '電話3',
            '單位類別',
            '聯絡人性質',
            '佣金',
            '編號',
            '間隔'
        ]
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
            '碧荔道': '薄扶林',
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
        self.items=[]
    def get_page(self):
        for i in range(1,self.page+1):
            self.pages.put(i)

    def get_urls(self):
        while not self.pages.empty():
            i = self.pages.get()
            print('852-Downloading by page %s' % i, '剩余%s' % self.pages.qsize())
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            web_driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe',                                          chrome_options=chrome_options)
            try:
                time.sleep(random.random())
                url = 'https://www.852.house/zh/properties?page=' + str(i)
                web_driver.get(url=url)
                time.sleep(1)
                webs = web_driver.find_elements_by_xpath('//*[@class="props-list list-group-item pos-relative"]')
                for url in webs:
                    url = url.get_attribute('href')
                    self.url.put(url)
                print('852-成功抓取%s個網址!' % self.url.qsize())
                web_driver.implicitly_wait(5)
                web_driver.close()
                self.pages.task_done()
            except:
                print('852-Retry……by page %s'%i)
                web_driver.close()
                time.sleep(2)
                self.pages.task_done()
                self.pages.put(i)
                return self.get_urls()

    def delnum(self):

        conn = mysql.connector.connect(host=self.ip, user='spider', password='123456', database='spider')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM spider852 WHERE datediff(curdate(), days)>=14')  # 删除旧编号
        cursor.execute('select * from spider852')
        values = cursor.fetchall()
        for v in values:
            self.newnum.append(v[0])
        conn.commit()
        cursor.close()
        conn.close()



    def addnum(self,id):
        if id not in self.newnum:
            self.newnum.append(id)
            return True
        else:
            return False


    def get_house(self,ret=1):

        while not self.url.empty():
            url = self.url.get()
            conn = mysql.connector.connect(host=self.ip, user='spider', password='123456', database='spider')
            cursor = conn.cursor()
            t3 = time.strftime("%Y-%m-%d", time.localtime())
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            web_driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe',
                                          chrome_options=chrome_options)
            print('852-剩余%s个网址'%self.url.qsize())
            time.sleep(2)
            try:

                web_driver.get(url)
                id = web_driver.find_element_by_class_name('ref-number').text.split()[1]
            except:
                if ret < 3 :
                    time.sleep(5)
                    self.url.task_done()
                    self.url.put(url)
                    print('852-重试%s'%ret)
                    return self.get_house(ret=ret+1)
                else:
                    print('852-重连超过2次，放弃此URL')
                    self.url.task_done()
                    return self.get_house()
            if self.addnum(id) is False:
                self.url.task_done()
                web_driver.close()
                return self.get_house()
                # 抓取聯繫人姓名和電話
            name = web_driver.find_elements_by_xpath('//div[@class="agent_name text-medium"]')
            company = web_driver.find_elements_by_class_name('agent_co')
            for i in name:
                name = i.text
            for i in company:
                company = i.text.split()
            if company != []:
                if name != ' ' and '-' not in company[0]:
                    name = name + ',' + company[0]
                if name == ' ' and '-' not in company[0]:
                    name = company[0]
            if name == ' ' and company == []:
                name = ''
            if re.findall(u'A-Za-z', name) == []:
                name = name.replace(' ', '')
            #時間
            data=time.strftime('%d/%m/%Y', time.localtime(time.time()))
            # 抓取售價和租價
            price = web_driver.find_element_by_class_name('color-1').text.split()[1]
            rent = web_driver.find_element_by_class_name('color-2').text.split()[1]
            if price == '-':
                situation = '租'
            elif rent == '-':
                situation = '售'
            else:
                situation = '租售'
            price = re.sub('萬', '', price)
            price = re.sub(',', '', price).replace('-','').replace('可議價','')
            if '億' in price:
                price = str(float(re.sub('億', '', price)) * 10000)
                price = str(Decimal(price).quantize(Decimal('0'))).replace('-','').replace('可議價','')
            rent = re.sub('萬', '0000', rent).replace('-','').replace('可議價','')
            # 抓取面積
            all_area = web_driver.find_elements_by_class_name('grey-big')
            area = []
            for i in all_area:
                area.append(i.text)
            b_area = area[0].replace("-","")
            p_area = area[1].replace("-","")
            if '呎' in b_area:
                b_area = b_area.replace('呎', '')
            if '呎' in p_area:
                p_area = p_area.replace('呎', '')
                # 抓取性質和備註
            pr_note = web_driver.find_elements_by_class_name('content-text')
            other_feature = web_driver.find_element_by_xpath(
                '//span[contains(text(),"其他特色")]/parent::*/../td[2]').text
            all_note = []
            for i in pr_note:
                all_note.append(i.text)
            if len(all_note) == 3:
                all_note[1] = all_note[1] + ',' + all_note[2]
            try:
                character = all_note[0].replace('盤', '')
            except:
                character = ''
            if len(all_note) > 1 and other_feature != '':
                if '，' in other_feature:
                    note = all_note[1].replace(' ', '') + ',' + re.sub(' ', '', other_feature)
                else:
                    note = all_note[1].replace(' ', '') + ',' + re.sub(' ', ',', other_feature)
            elif len(all_note) > 1 and other_feature == '':
                note = all_note[1].replace(' ', '')
            else:
                if ' ' in other_feature:
                    note = other_feature.replace(' ', ',')
                else:
                    note = other_feature
            # print (name,'1')

            tel = web_driver.find_elements_by_xpath('//div[@class="row tel"]')
            for i in tel:
                tel = i.text
            tel = re.sub(' ', '', tel)
            source='852'
            usage = web_driver.find_element_by_class_name('tag-content').text.replace("工業","工廈").replace("舖位","商舖")

            try:
                property = web_driver.find_element_by_xpath('//div[@class="page-title-p"]/h1').text
            except:
                web_driver.refresh()
                time.sleep(1)
                try:
                    property = web_driver.find_element_by_xpath('//div[@class="page-title-p"]/h1').text
                except:
                    continue
            adress = web_driver.find_element_by_xpath('//div[@class="page-title-p"]/span').text
            try:
                loca = web_driver.find_element_by_xpath('//span[contains(text(),"詳細地址")]/../../td[2]').text.split()[2].replace("大埔","大埔墟")
            except:
                loca = ''
            zone=self.dic.get(loca)
            if len(adress.replace(loca,
                                  '')) > 2 and '黃竹坑道' not in adress and '太子道' not in adress and '香港仔大道' not in adress and '馬頭角道' not in adress and '何文田街' not in adress and '牛頭角道' not in adress and '大潭道' not in adress and '長沙灣道' not in adress:
                adress = adress.replace(loca, '')
            item=[data,source,situation,rent,price,p_area,b_area,zone,loca,adress,property,None,None,None,None,None,note,name,tel,None,None,None,None,usage,character,None,id,None]
            print('852-',item)
            cursor.execute('INSERT into spider852 VALUES("%s","%s")' % (id, t3))
            conn.commit()
            self.items.append(item)
            self.url.task_done()
            web_driver.close()
            cursor.close()
            conn.close()

    def pri(self):
        df=pd.DataFrame(self.items,columns=self.columns)
        df.to_excel(r'C:\Users\Administrator\Desktop\jianbao\每日\852.xlsx',index=None)
        print('852-输出完成')


    def run(self):
        self.get_page()
        geturllist=[]
        for i in range(7):
            geturlthr=threading.Thread(target=self.get_urls)
            geturllist.append(geturlthr)
        for t in geturllist:
            t.setDaemon(True)
            t.start()
        for t in geturllist:
            t.join()
        self.delnum()
        gethouselist=[]
        print('开始爬取页面')
        for i in range(3):
            gethousethr=threading.Thread(target=self.get_house)
            gethouselist.append(gethousethr)
        for t in gethouselist:
            t.setDaemon(True)
            t.start()
        for t in gethouselist:
            t.join()
        print('抓取完成')
        # self.prinum()
        self.pri()

if __name__ == '__main__':
    eft=eft(7)
    eft.run()
    # eft.delnum()