import requests
import json
import jsonpath
import pandas as pd
import time
import chardet
from lxml import html


class midland:
    def __init__(self):
        self.items = []
        self.columns = [
            '中文名',
            '職別',
            '英文名',
            '所屬公司',
            '分行地址',
            '香港電話',
            '大陸電話',
            '虛擬電話',
            '代理牌照',
            '郵件']

    def req(self, a, reties=1):
        try:
            url = r'https://apis.midland.com.hk/api/agent/list?page=%s&limit=10&total=Y&lang=zh-HK&show_award=Y&show_cert=Y&sort=GROUP_RANK' % a
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
            }
            req = requests.session().get(url, headers=headers)
        except Exception as e:
            print('第一次重連%s' % reties)
            return self.req(a, reties + 1)
        dic = json.loads(req.text)
        names = jsonpath.jsonpath(dic, '$..chi_name')
        titles = jsonpath.jsonpath(dic, '$..title')
        en_names = jsonpath.jsonpath(dic, '$..eng_name')
        dept_names = jsonpath.jsonpath(dic, '$..dept_name')
        tel_hks = jsonpath.jsonpath(dic, '$..tel_hk')
        tel_prcs = jsonpath.jsonpath(dic, '$..tel_prc')
        emails = jsonpath.jsonpath(dic, '$..email')
        virtual_phone_nos = jsonpath.jsonpath(dic, '$..virtual_phone_no')
        licence_nos = jsonpath.jsonpath(dic, '$..licence_no')
        com = '美聯物業'
        for i in range(0, len(names)):
            item = [
                names[i],
                titles[i],
                en_names[i],
                com,
                dept_names[i],
                tel_hks[i],
                tel_prcs[i],
                virtual_phone_nos[i],
                licence_nos[i],
                emails[i]]
            self.items.append(item)
            print(item)
        df = pd.DataFrame(self.items, columns=self.columns)
        df.to_excel(
            r'C:\Users\Administrator\Desktop\经纪人爬取\美聯-index.xlsx',
            index=None)


if __name__ == '__main__':
    midland = midland()
    for a in range(1, 126):
        print(a)
        time.sleep(2)
        midland.req(a)
