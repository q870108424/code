from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from decimal import Decimal
import pandas as pd
import selenium
import datetime
import random
import time
import re
import os
import random
from pykeyboard import *
from pymouse import *
import threading

'''可能需要更改代码'''
class eprcpr:
    def __init__(self):
        self.id_password = {#待使用账号
            }
        self.id_password={}
        self.web_driver=webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe')

    def login(self):
        id=random.choice(list(self.id_password.keys()))
        pw=self.id_password.get(id)
        print('Logining...')
        print('正在使用賬號 %s 登錄' % id)
        url=r'http://eprc.com.hk/eprcLogin.html'
        self.web_driver.get(url)
        self.web_driver.maximize_window()
        self.web_driver.switch_to.frame('topFrame')
        username = self.web_driver.find_element_by_class_name('loginC')  # 账号框
        username.click()
        time.sleep(1)
        username.send_keys(id)
        time.sleep(1)
        password = self.web_driver.find_element_by_xpath('//input[@name="password"]')  # 密码框
        password.click()
        time.sleep(1)
        password.send_keys(pw)
        time.sleep(10)
        # code_1 = self.web_driver.find_element_by_xpath('//input[@id="corporateCode"]')  # 企业码框
        # code_1.send_keys('w148')
        # code_2 = web_driver.find_element_by_xpath('//input[@name="jcaptcha"]')
        # code_2.send_keys(input('請輸入驗證碼2：')))
        password.send_keys(Keys.ENTER)
        self.web_driver.switch_to.default_content()
        self.web_driver.switch_to.frame('topFrame')
        # 跳轉
        try:
            time.sleep(1)
            self.web_driver.find_element_by_id('menu_4')
            print('登錄成功')
        except:
            print('登錄失敗,刷新重試...')
            self.web_driver.refresh()
            return self.login()

    def Switch(self):
        self.web_driver.refresh()
        self.web_driver.switch_to.frame('topFrame')
        time.sleep(random.uniform(1, 2))
        self.web_driver.find_element_by_id('menu_4').click()
        time.sleep(0.5)
        time.sleep(random.uniform(1, 2))
        self.web_driver.switch_to.frame('iframe_content')
        time.sleep(random.uniform(0.5, 1))

    def choice(self):
        days=self.web_driver.find_element_by_id('updateDate')
        days.click()
        days.find_element_by_xpath("//option[@value='1']").click()
        time.sleep(1.2)
        for dis in ['HK,HK-KT,HK-SYP,HK-SW,HK-C,HK-P,HK-WC,HK-CB,HK-HV,HK-NP,HK-QB,HK-SKW,HK-CW,HK-SSW,HK-MW,HK-MLC,HK-NPH,HK-MLE,HK-TT,HK-SL,HK-RB,HK-WCH,HK-A,HK-PFL','KL,KL-TST,KL-YMT,KL-MK,KL-TKT,KL-SKM,KL-SSP,KL-CSW,KL-LCK,KL-HH,KL-HMT,KL-KTK,KL-KC,KL-KL,KL-WTH,KL-WTS,KL-TWS,KL-DH,KL-SPK,KL-NCW,KL-KB,KL-NTK,KL-KT,KL-LT,KL-KYT','NT,NT-ST,NT-MOS,NT-TP,NT-FL,NT-SS,NT-KC,NT-TY,NT-TW,NT-TM,NT-YL,NT-TKO,NT-SK,NT-ISL']:
            cho1=self.web_driver.find_element_by_id('district')
            cho1.click()
            time.sleep(1.01)
            ele1="//option[@value='{}']".format(dis)
            cho1.find_element_by_xpath(ele1).click()
            time.sleep(1.7)
            for usage in ['RES','OFC','COM','IND','CPS']:
                cho=self.web_driver.find_element_by_id('usage')
                cho.click()
                time.sleep(1)
                ele="//option[@value='{}']".format(usage)
                cho.find_element_by_xpath(ele).click()
                print('正在爬取%s-%s'%(dis[0:2],usage))
                time.sleep(1)
                self.web_driver.find_element_by_xpath('//a[@class="btnSearch btnSearch-primary rounded-corners"]').click()
                time.sleep(1)
                self.Get_house()
                self.Switch()

    def run(self):
        print('即將定位預覽列印鍵')
        print_2 = self.web_driver.find_element_by_xpath('//*[@id="printLoc"]').click()
        print('定位預覽列印鍵完成')

    def run2(self):
        print('即將定位保存鍵')
        m = PyMouse()
        m.click(200, 170, 1)
        print('定位保存鍵完成')

    def run3(self):
        print('即將定位保存文件名選項框')
        m = PyMouse()
        m.click(800, 650, 1)
        m.click(800, 650, 1)
        print('定位保存文件名選項框完成')

    def run4(self,i):
        now_time = datetime.datetime.now().strftime('%Y%m%d')
        k = PyKeyboard()
        time.sleep(1)
        k.type_string('%sEPRC叫價盤列印第%d頁' % (now_time, i))
        time.sleep(1)
        k.tap_key(k.enter_key)
        print('保存完成')

    def run5(self):
        print('即將定位文件夾')
        m = PyMouse()
        m.click(800, 500, 1)
        m.click(800, 500, 1)
        print('定位文件夾完成')
    def Get_house(self):
        try:
            # 按更新時間排序
            self.web_driver.find_element_by_xpath(
                '//*[@id="AskingForm"]/table[3]/tbody/tr[2]/td/table/tbody/tr[2]/td/a').click()
            self.web_driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td/form/table[1]/tbody/tr[2]/td[1]/select/option[11]').click()
            self.web_driver.find_element_by_xpath(
                '/html/body/table/tbody/tr/td/form/table[1]/tbody/tr[2]/td[2]/input').click()
            self.web_driver.find_element_by_xpath('/html/body/table/tbody/tr/td/form/table[1]/tbody/tr[4]/td/a').click()
            print('按更新時間排列')
            start1 = time.time()

            # 抓取-----------------------------------------
            next = self.web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
            count_page = 0
            for i in next:
                count_page += 1
                if count_page == 6:
                    print('即將切換至末頁')
                    time.sleep(random.uniform(1, 5))
                    i.click()
                continue

            try:
                total_building = self.web_driver.find_element_by_xpath('//font[@class="txtChi17 pageRecordCountColor"]').text
                total_building = re.findall(u'\d*\)', total_building)[0].replace(')', '')
            except:
                total_building = '0'
            print('叫價盤物業共%s' % total_building)

            total_building = int(total_building)
            # 點擊頁碼次數
            page_click = int(total_building / 30)
            if total_building % 30 == 0:
                page_click -= 1

            now_time = datetime.datetime.now().strftime('%Y%m%d')
            n = 1
            for i in range(1, page_click + 2):
                print_1 = self.web_driver.find_element_by_xpath(
                    '//*[@id="AskingForm"]/table[3]/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/nobr/a[1]').click()
                time.sleep(3)
                t1 = threading.Thread(target=self.run)
                t1.start()
                time.sleep(3)
                t2 = threading.Thread(target=self.run2)
                t2.start()
                time.sleep(3)
                if i == 1:
                    t5 = threading.Thread(target=self.run5)
                    t5.start()
                    time.sleep(3)
                t3 = threading.Thread(target=self.run3)
                t3.start()
                time.sleep(3)
                t4 = threading.Thread(target=self.run4, args=(i,))
                t4.start()
                time.sleep(3)
                self.web_driver.back()
                time.sleep(3)
                self.web_driver.switch_to.default_content()
                self.web_driver.switch_to.frame('topFrame')
                self.web_driver.switch_to.frame('iframe_content')
                time.sleep(3)
                n += 1
                next = self.web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
                if len(next) == 0:
                    time.sleep(5)
                    self.web_driver.switch_to.default_content()
                    self.web_driver.switch_to.frame('topFrame')
                    self.web_driver.switch_to.frame('iframe_content')
                    time.sleep(3)
                    next = self.web_driver.find_elements_by_xpath('//img[@style="vertical-align: middle;"]')
                # print('next長度:', len(next))
                count_page = 0
                for i in next:
                    count_page += 1
                    if count_page == 4:
                        print('即將切換至第-%d頁' % n)
                        time.sleep(random.uniform(1, 2))
                        i.click()
                    continue
                time.sleep(1)
        except Exception as e:
            print(e)
            pass


if __name__ == '__main__':
    kk=eprcpr()
    kk.login()
    kk.Switch()
    kk.choice()
