from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.chrome.options import Options
class Ljg:
    def __init__(self):
        self.links=[]

    def sel(self,i):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        url=r'https://property.ricacorp.com/post;language=HK;page=%s;paymentPeriod=30;mortgageInterestRate=2.375'%i
        web_driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
        web_driver.get(url)
        time.sleep(3)
        links=web_driver.find_elements_by_xpath('/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand/div/div/div/div[2]/div/div/app-secondhand-list/a')
        for link in links:
            self.links.append(link.get_attribute('href'))
        df=pd.DataFrame({'links':self.links})
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\二手.xlsx', index=None)
        web_driver.close()

    def allman(self,url):
        web_driver.get(url)
        web_driver.maximize_window()
        time.sleep(3)
        links = web_driver.find_elements_by_xpath(
            '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]//div/div[1]/div[1]/app-secondhand-details-agent-details/div/img')
        if len(links)==1:
            web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[2]/div[2]/button[2]/span/div/div/span').click()
            tel1 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[2]/div[2]/button[2]/span/div/div/span').text
            name1=web_driver.find_element_by_xpath('/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[1]').text
            en_name1=web_driver.find_element_by_xpath('/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[2]').text
            id1=web_driver.find_element_by_xpath('/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[3]').text
            adress1=web_driver.find_element_by_xpath('/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[4]').text
            com = '利嘉閣'
            item=[name1,en_name1,id1,com,adress1,tel1]
            print(item)
            self.links.append(item)

        elif len(links) == 2:
            web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[2]/div[2]/button[2]/span/div/div/span').click()
            web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[2]/div[2]/button[2]/span/div/div/span').click()
            tel1=web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[2]/div[2]/button[2]/span/div/div/span').text
            tel2 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[2]/div[2]/button[2]/span/div/div/span').text
            name1 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[1]').text
            en_name1 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[2]').text
            id1 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[3]').text
            adress1 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[1]/div[1]/div[2]/div[4]').text
            name2= web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[1]/div[2]/div[1]').text
            en_name2 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[1]/div[2]/div[2]').text
            id2 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[1]/div[2]/div[3]').text
            adress2 = web_driver.find_element_by_xpath(
                '/html/body/app-root/app-layout/div/div[1]/mat-sidenav-container/mat-sidenav-content/app-secondhand-details/div/div[2]/div[1]/div[2]/app-secondhand-details-agent/div[1]/div[2]/div/div[1]/div[2]/div[4]').text
            com='利嘉閣'
            item=[[name1,en_name1,id1,com,adress1,tel1],[name2,en_name2,id2,com,adress2,tel2]]
            for itw in item:
                self.links.append(itw)
                print(itw)
        df = pd.DataFrame(self.links,columns=['中文名','英文名','代理牌照','所屬公司','分行地址','電話'])
        df.to_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\利嘉閣代理.xlsx', index=None)



if __name__ == '__main__':
    ljg=Ljg()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    web_driver = webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
    df = pd.read_excel(r'C:\Users\Administrator\Desktop\经纪人爬取\利嘉閣二手.xlsx').values.tolist()
    g=0
    for url in df:
        g+=1
        url=url[0]

        print(g,url)
        ljg.allman(url)
