from selenium import webdriver
import random
import time
from tkinter import *
import re
import zipfile
import os
import threading
from PIL import Image
import pytesseract
import datetime
import requests
from pykeyboard import *
from pymouse import PyMouse
from selenium.webdriver.common.keys import Keys
class EPRCPRI(threading.Thread):
    def __init__(self):
        # account='''         库存账号
        # self.id_password = {  # 待使用账号

        # }
        self.id_password={}
		#保安密碼  



    def webd(self):
        global web_driver
        web_driver = webdriver.Chrome(r'C:\Users\Administrator\Desktop\python\chromedriver.exe')

    def login(self):
        id = random.choice(list(self.id_password.keys()))
        pw = self.id_password.get(id)
        print('Logining...')
        print('正在使用賬號 %s 登錄' % id)
        url = r'http://eprc.com.hk/eprcLogin.html'
        web_driver.get(url)
        web_driver.maximize_window()
        web_driver.switch_to.frame('topFrame')
        username = web_driver.find_element_by_class_name('loginC')  # 账号框
        username.click()
        time.sleep(1)
        username.send_keys(id)
        time.sleep(1)
        password = web_driver.find_element_by_xpath('//input[@name="password"]')  # 密码框
        password.click()
        time.sleep(1)
        password.send_keys(pw)
        time.sleep(1)
        cos=self.save_code()#验证码识别
            # code_1 = web_driver.find_element_by_xpath('//input[@id="corporateCode"]')  # 企业码框
            # code_1.send_keys('w148')
            # time.sleep(1)
            # code_1.send_keys(Keys.ENTER)
        code=web_driver.find_element_by_xpath('//input[@id="verificationCode"]')#验证码框
        code.send_keys(cos)
        time.sleep(1)
        try:
            code.send_keys(Keys.ENTER)

            web_driver.switch_to.default_content()
            web_driver.switch_to.frame('topFrame')
            # 跳轉

            time.sleep(1)
            web_driver.find_element_by_id('menu_4')
            print('登錄成功')
        except:
            print('登錄失敗,刷新重試...')
            web_driver.refresh()
            return self.login()

    def Switch(self):
        web_driver.refresh()
        web_driver.switch_to.frame('topFrame')
        time.sleep(random.uniform(1, 2))
        web_driver.find_element_by_id('menu_4').click()
        time.sleep(0.5)
        web_driver.find_element_by_id('sub_menu_4_26').click()  # 点击最新租售
        time.sleep(random.uniform(1, 2))
        web_driver.switch_to.frame('iframe_content')  # 再次切换到Frame
        time.sleep(random.uniform(0.5, 1))
        web_driver.find_element_by_xpath('//a[@class="btn btn-primary rounded-corners"]').click()  # 点击搜寻

    def calc_page(self):
        try:
            total_building = web_driver.find_element_by_xpath('//font[@class="txtChi17 pageRecordCountColor"]').text
            total_building = re.findall(u'\d*\)', total_building)[0].replace(')', '')#提取叫价盘数目
            total_building = int(total_building)
            # 點擊頁碼次數
            print('叫價盤物業共%s' % total_building)
            page_click = int(total_building / 30)
            if total_building % 30 == 0:
                page_click = page_click-1
            print('共%s页' % (page_click + 1))
            return page_click+1
        except:
            page_click = 0
        return page_click
    def enter_tosave(self):
        m = PyMouse()
        m.click(200, 170, 1)
        print('定位保存鍵完成')

    def frist_topri(self):
        print('即將定位文件夾并下载第一页')
        m = PyKeyboard()
        for i in range(5):
            m.tap_key(m.tab_key)
            time.sleep(1)
        m.tap_key(m.space_key)
        time.sleep(1)
        m.type_string(r'C:\Users\Administrator\Downloads\eprcpri')
        time.sleep(1)
        m.tap_key(m.enter_key)
        m.tap_key(m.enter_key)
        print('定位文件夾完成')
        time.sleep(1)
        for i in range(6):
            m.tap_key(m.tab_key)
            time.sleep(1)
        self.second_topri()


    def RandomPasswd(self,rang=None):
        __numlist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'q', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
                     'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'W', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                     'Y', 'Z']
        if rang == None:
            _Passwd = "".join(random.choice(__numlist) for i in range(8))
        else:
            _Passwd = "".join(random.choice(__numlist) for i in range(int(rang)))
        return _Passwd

    def second_topri(self):
        now_time = datetime.datetime.now().strftime('%Y%m%d')
        k = PyKeyboard()
        names = self.RandomPasswd(rang=10)
        filename = '%sEPRC-%s' % (now_time, names)
        for word in filename:
            k.tap_key(word)
            time.sleep(0.1)
        k.tap_key(k.space_key)
        time.sleep(1)
        k.tap_key(k.enter_key)
        print('保存完成')

    def click_pri(self,n):
        try:
            web_driver.find_element_by_xpath(
                '//*[@id="AskingForm"]/table[3]/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/nobr/a[1]').click()  # 点击预览列印
            time.sleep(3)
            web_driver.find_element_by_xpath('//*[@id="printLoc"]').click()  # 点击打印
            print('点击打印完成')
        except Exception as e:
            res=threading.Thread(target=self.retry,args=(n,))
            res.start()
            res.join()

    def print(self):
        page_click = self.calc_page()#获取页码
        if page_click == 0:
            print('无数据')
            self.loginout()
            return
        next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
        i = next[5]
        print('即將切換至末頁')
        time.sleep(random.uniform(1, 5))
        i.click()
        n = 1
        for pa in range(1, page_click + 1):
            # self.click_pri()
            t0=threading.Thread(target=self.click_pri,args=(n,))
            t0.start()
            # t0.join()#此处不能阻塞 保存完成前都不能算完成此函数
            time.sleep(20)
            print('即将点击保存')
            t1=threading.Thread(target=self.enter_tosave)
            t1.start()
            t1.join()
            time.sleep(3)
            if pa == 1:
                t2=threading.Thread(target=self.frist_topri)
                t2.start()
            else:
                t2=threading.Thread(target=self.second_topri)
                t2.start()
            t2.join()
            time.sleep(2)
            try:
                web_driver.implicitly_wait(10)
                web_driver.find_element_by_xpath('//*[@id="backbtn"]').click()#点击返回
            except Exception as e:
                res = threading.Thread(target=self.retry, args=(n,))
                res.start()
                res.join()
            web_driver.switch_to.default_content()
            web_driver.switch_to.frame('topFrame')
            web_driver.switch_to.frame('iframe_content')
            time.sleep(2)
            n += 1
            next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
            if len(next) == 0:
                web_driver.switch_to.default_content()
                web_driver.switch_to.frame('topFrame')
                web_driver.switch_to.frame('iframe_content')
                time.sleep(3)
                next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
            try:
                print('即將切換至第-%d頁' % n)
                time.sleep(random.uniform(1, 2))
                ite=next[3]
                ite.click()
            except Exception as e:
                res = threading.Thread(target=self.retry, args=(n,))
                res.start()
                res.join()
            time.sleep(2)
        print('列印完成')
    def retry(self,n):
        print('返回重試')
        web_driver.refresh()
        time.sleep(2)
        self.Switch()
        web_driver.implicitly_wait(10)
        time.sleep(2)
        next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
        next[5].click()
        web_driver.implicitly_wait(10)
        print('切換至上次中斷的頁碼')
        for num in range(n - 1):
            next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
            if len(next) == 0:
                web_driver.switch_to.default_content()
                web_driver.switch_to.frame('topFrame')
                web_driver.switch_to.frame('iframe_content')
                time.sleep(3)
                next = web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
            web_driver.implicitly_wait(10)
            time.sleep(1)
            next[3].click()

    def start_to_print(self):
        self.webd()
        self.login()
        self.Switch()
        self.print()

    def save_code(self):
        web_driver.get_screenshot_as_file(r'D:\1.png')
        size=web_driver.find_element_by_id('vImage').size
        location=web_driver.find_element_by_id('vImage').location
        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        a = Image.open(r'D:\1.png')
        im = a.crop((left, top, right, bottom))
        im.save(r'D:\2.png')
        imgs = Image.open(r'D:\2.png').convert("L")
        img=self.twoz(imgs)
        vcode = pytesseract.image_to_string(img).replace(" ","")
        time.sleep(1)
        if len(vcode)==4:
            return vcode
        else:
            print('识别失败刷新验证码')
            web_driver.find_element_by_id('vImage').click()
            return self.save_code()
    def twoz(self,img):
        pixdata = img.load()
        w, h = img.size
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] > 110:
                    pixdata[x, y] = 255
                else:
                    pixdata[x, y] = 0
        return img
    # def start(self):
    #     self.webd()
    #     p=threading.Thread(target=self.start_to_print)
    #     r=threading.Thread(target=self.root)
    #     r.start()
    #     time.sleep(1)
    #     p.start()
    #     p.join()
    def forzip(self):
        try:
            now_time = datetime.datetime.now().strftime('%Y%m%d')
            startdir = r"C:\Users\Administrator\Downloads\eprcpri" # 要压缩的文件夹路径
            file_news = startdir + '/' + now_time + 'EPRC叫價盤列印.zip'  # 压缩后文件夹的名字
            z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirnames, filenames in os.walk(startdir):
                fpath = dirpath.replace(startdir, '')
                fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if '.pdf' in filename:
                    z.write(os.path.join(dirpath, filename), fpath + filename)
            print('压缩成功')
            z.close()
            os.startfile(r"C:\Users\Administrator\Downloads\eprcpri")
        except Exception as e:
            print('列印失败了')
    def delpdf(self):
        startdir = r"C:\Users\Administrator\Downloads\eprcpri"  # 要压缩的文件夹路径
        for dirpath, dirnames, filenames in os.walk(startdir):
            for filename in filenames:
                if '.pdf' in filename:
                    dir = startdir + '/' + filename
                    os.remove(dir)

    def run(self):
        self.start_to_print()
        self.loginout()
        self.pdf2excel(r"C:\Users\Administrator\Downloads\eprcpri")
        self.forzip()

    def pdf2excel(self,path):
        url = r'http://localhost:8111/pdf2excel/upload'
        fromdata = {
            'pdfDir': path
        }
        response = requests.session().post(url, data=fromdata)
        print(response.text)

    def loginout(self):
        try:
            cookies = web_driver.get_cookies()
            cookies_title = cookies[0].get('name')
            cookies_index = cookies[0].get('value')
            cookies = cookies_title + '=' + cookies_index
            headers={
                'Host':'eprc.com.hk',
                'Connection':'keep-alive',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Referer':'http://eprc.com.hk/EprcWeb/multi/transaction/login.do;jsessionid=%s'%cookies_index,
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Cookie':cookies

            }
            url=r'http://eprc.com.hk/EprcWeb/multi/transaction/logout.do'
            req=requests.session().get(url,headers=headers)
            web_driver.refresh()
            print(req.status_code)
            print('登出成功')
        except Exception as e:
            print('登出失败')
if __name__ == '__main__':
    epr=EPRCPRI()
    epr.run()
