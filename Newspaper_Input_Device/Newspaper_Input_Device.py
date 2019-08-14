import pandas as pd
import time
import os
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import *
import datetime
import copy


class Newspaper:
    def __init__(self):
        self.new = []
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
            '間隔',
            '電話核實狀態',
            '電話情況']
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

    def read(self):
        global dic
        global df
        waits.title('加載中……')
        sys = []
        try:
            df = pd.read_excel(r'C:\Users\Administrator\Desktop\剪報20181211始.xlsx')
        except:
            self.warming('没找到文件加载')
            waits.title('登錄')
            return
        for a in df.index:
            sys.append(a)
        days = list(df['日期'].values)
        names = list(df['物業名稱'].values)
        tels = list(df['電話1'].values)
        locas = list(df['地段'].values)
        prices = list(df['售價'].values)
        rents = list(df['租金'].values)
        adresss = list(df['街道'].values)
        dic = dict()
        for i in range(0, len(days)):
            inde = []
            day = days[i]
            price = prices[i]
            rent = rents[i]
            tel = tels[i]
            loca = locas[i]
            name = names[i]
            adress = adresss[i]
            sy = sys[i]
            inde.append(day)
            inde.append(loca)
            inde.append(name)
            inde.append(tel)
            inde.append(price)
            inde.append(rent)
            inde.append(adress)
            inde.append(sy)
            if (tel in dic.keys()):
                vas = dic.get(tel)
                dic.update({tel: vas + [inde]})
            else:
                dic.update({tel: [inde]})
        waits.destroy()
        self.main()
        return dic

    def show(self, *args):
        for i in args:
            text.insert(END, i)
            text.see(END)
            text.update()

    def times(self, i):
        t1 = i[0].split("/")
        time1 = t1[2] + '-' + t1[1] + '-' + t1[0]
        t1 = datetime.datetime.strptime(time1, '%Y-%m-%d')
        t2 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        t2 = datetime.datetime.strptime(t2, '%Y-%m-%d')
        days = (t2 - t1).days
        days = str(days) + '天'
        return days

    def select(self):
        global row
        global s
        showds = []
        row = None
        t = telinput.get()
        try:
            t = int(t)
        except Exception as e:
            self.show('錯誤，請檢查電話是否為純數字！')
            return
        s = dic.get(t)
        if s is not None:
            text.delete(0, END)
            self.show('距今  地段   物業名    電話    租金    售價    地址    索引')
            for i in s:
                showd = copy.copy(i)
                showd[0] = self.times(i)
                # showds.append(showd)
                self.show(showd)
            # df=pd.DataFrame(showds,columns=['距今','地段','物業名','電話','租金','售價','地址','索引'])
            # for d in df.values:
            #     self.show(d)
        else:
            self.show('電話不存在！')

    def addmain(self):
        global adroot, source, sta, usage, status, rentmy, price, area1, area2, loca, propertys, adress, qi, build, floor, room, carnum, tip, name1, tel1, name2, tel2, jiange, loca2
        adroot = Tk()
        adroot.title('新增')
        adroot.geometry('900x300+898+79')
        source = ttk.Combobox(adroot, state='readonly')
        source.place(relx=0.1, rely=0.1, anchor=CENTER)
        source['value'] = ('星島', '經濟', '東方')
        source.current(0)
        sta = ttk.Combobox(adroot, state='readonly')
        sta.place(relx=0.1, rely=0.2, anchor=CENTER)
        sta['value'] = ('租', '售', '租售')
        sta.current(0)
        usage = ttk.Combobox(adroot, state='readonly')
        usage.place(relx=0.1, rely=0.3, anchor=CENTER)
        usage['value'] = ('住宅', '工廈', '商舖', '寫字樓', '車位', '土地')
        usage.current(0)
        status = ttk.Combobox(adroot, state='readonly')
        status.place(relx=0.1, rely=0.4, anchor=CENTER)
        status['value'] = ('業主', '代理')
        status.current(0)
        button4 = Button(
            adroot,
            text='導入區域',
            font=(
                "微软雅黑",
                15),
            command=self.writloca2,
            activebackground='yellow').place(
            relx=0.1,
            rely=0.55,
            anchor=CENTER)
        Label(
            adroot,
            text='租金',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.1,
            anchor=CENTER)
        rentmy = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        rentmy.place(relx=0.34, rely=0.1, anchor=CENTER)
        Label(
            adroot,
            text='售價',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.25,
            anchor=CENTER)
        price = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        price.place(relx=0.34, rely=0.25, anchor=CENTER)
        Label(
            adroot,
            text='實呎',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.4,
            anchor=CENTER)
        area1 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        area1.place(relx=0.34, rely=0.4, anchor=CENTER)
        Label(
            adroot,
            text='建呎',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.55,
            anchor=CENTER)
        area2 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        area2.place(relx=0.34, rely=0.55, anchor=CENTER)
        Label(
            adroot,
            text='地段',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.85,
            anchor=CENTER)
        loca = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        loca.place(relx=0.34, rely=0.85, anchor=CENTER)
        Label(
            adroot,
            text='區域',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.22,
            rely=0.7,
            anchor=CENTER)
        loca2 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        loca2.place(relx=0.34, rely=0.7, anchor=CENTER)
        Label(
            adroot,
            text='物業名',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.455,
            rely=0.05,
            anchor=CENTER)
        propertys = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        propertys.place(relx=0.59, rely=0.05, anchor=CENTER)
        Label(
            adroot,
            text='期',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.45,
            rely=0.203,
            anchor=CENTER)
        qi = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        qi.place(relx=0.59, rely=0.203, anchor=CENTER)
        Label(
            adroot,
            text='座',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.45,
            rely=0.358,
            anchor=CENTER)
        build = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        build.place(relx=0.59, rely=0.358, anchor=CENTER)
        Label(
            adroot,
            text='樓層',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.45,
            rely=0.513,
            anchor=CENTER)
        floor = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        floor.place(relx=0.59, rely=0.513, anchor=CENTER)
        Label(
            adroot,
            text='室號',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.45,
            rely=0.668,
            anchor=CENTER)
        room = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        room.place(relx=0.59, rely=0.668, anchor=CENTER)
        Label(
            adroot,
            text='地址',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.45,
            rely=0.95,
            anchor=CENTER)
        adress = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        adress.place(relx=0.59, rely=0.95, anchor=CENTER)
        Label(
            adroot,
            text='聯繫人1',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.1,
            anchor=CENTER)
        name1 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        name1.place(relx=0.87, rely=0.1, anchor=CENTER)
        Label(
            adroot,
            text='電話1',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.25,
            anchor=CENTER)
        t = telinput.get()
        tel1 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        tel1.place(relx=0.87, rely=0.25, anchor=CENTER)
        tel1.insert(10,t)
        Label(
            adroot,
            text='聯繫人2',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.4,
            anchor=CENTER)
        name2 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        name2.place(relx=0.87, rely=0.4, anchor=CENTER)
        Label(
            adroot,
            text='電話2',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.55,
            anchor=CENTER)
        tel2 = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        tel2.place(relx=0.87, rely=0.55, anchor=CENTER)
        Label(
            adroot,
            text='備註',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.7,
            anchor=CENTER)
        tip = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        tip.place(relx=0.87, rely=0.7, anchor=CENTER)
        Label(
            adroot,
            text='車位號碼',
            font=(
                "微软雅黑",
                8),
            fg='black',
            justify=LEFT).place(
            relx=0.46,
            rely=0.82,
            anchor=CENTER)
        carnum = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        carnum.place(relx=0.59, rely=0.823, anchor=CENTER)
        Label(
            adroot,
            text='間隔',
            font=(
                "微软雅黑",
                10),
            fg='black',
            justify=LEFT).place(
            relx=0.73,
            rely=0.85,
            anchor=CENTER)
        jiange = Entry(adroot, font=("微软雅黑", 10), fg='#04a89f')
        jiange.place(relx=0.87, rely=0.85, anchor=CENTER)
        button = Button(
            adroot,
            text='確認新增',
            font=(
                "微软雅黑",
                15),
            command=self.addpri,
            activebackground='yellow').place(
            relx=0.1,
            rely=0.9,
            anchor=CENTER)
        adroot.bind('<Key-Return>', self.addpri_enter)

    def copy(self):
        global row
        ind = text.curselection()
        columns = [
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
            '間隔',
            '電話核實狀態',
            '電話情況']
        if ind == ():
            self.show('請選中后再點擊')
        else:
            try:
                srow = text.get(ind)
                v = srow[-1]
                row = (df.loc[v].tolist())
                self.show('-' * 120)
                for i in range(0, len(row) - 2):
                    self.show('%s:%s' % (columns[i], row[i]))
            except Exception as e:
                self.show('未知錯誤，請聯繫管理員')
                self.show(e)

    def fix(self):
        global frow, source, sta, rentmy, price, area1, area2, loca, adress, propertys, qi, build, floor, room, carnum, tip, name1, tel1, name2, tel2, usage, status, fixroot, jiange, loca2
        if row is None:
            self.show('你還沒有選擇數據！')
        else:
            fixroot = Tk()
            fixroot.title('修改')
            fixroot.geometry('900x300+398+79')
            source = ttk.Combobox(fixroot, state='readonly')
            source.place(relx=0.1, rely=0.1, anchor=CENTER)
            source['value'] = ('星島', '經濟', '東方')
            a = self.revalue(1)
            source.current(a)
            sta = ttk.Combobox(fixroot, state='readonly')
            sta.place(relx=0.1, rely=0.2, anchor=CENTER)
            sta['value'] = ('租', '售', '租售')
            a = self.revalue(2)
            sta.current(a)
            usage = ttk.Combobox(fixroot, state='readonly')
            usage.place(relx=0.1, rely=0.3, anchor=CENTER)
            usage['value'] = ('住宅', '工廈', '商舖', '寫字樓', '車位', '土地')
            a = self.revalue(3)
            usage.current(a)
            status = ttk.Combobox(fixroot, state='readonly')
            status.place(relx=0.1, rely=0.4, anchor=CENTER)
            status['value'] = ('業主', '代理')
            a = self.revalue(4)
            status.current(a)
            button4 = Button(
                fixroot,
                text='導入區域',
                font=(
                    "微软雅黑",
                    15),
                command=self.writloca2,
                activebackground='yellow').place(
                relx=0.1,
                rely=0.55,
                anchor=CENTER)
            Label(
                fixroot,
                text='租金',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.1,
                anchor=CENTER)
            rentmy = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            rentmy.place(relx=0.34, rely=0.1, anchor=CENTER)
            rentmy.insert(10, self.fixrow(3))
            Label(
                fixroot,
                text='售價',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.25,
                anchor=CENTER)
            price = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            price.place(relx=0.34, rely=0.25, anchor=CENTER)
            price.insert(10, self.fixrow(4))
            Label(
                fixroot,
                text='實呎',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.4,
                anchor=CENTER)
            area1 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            area1.place(relx=0.34, rely=0.4, anchor=CENTER)
            area1.insert(10, self.fixrow(5))
            Label(
                fixroot,
                text='建呎',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.55,
                anchor=CENTER)
            area2 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            area2.place(relx=0.34, rely=0.55, anchor=CENTER)
            area2.insert(10, self.fixrow(6))
            Label(
                fixroot,
                text='地段',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.85,
                anchor=CENTER)
            loca = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            loca.place(relx=0.34, rely=0.85, anchor=CENTER)
            loca.insert(10, self.fixrow(8))
            Label(
                fixroot,
                text='區域',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.22,
                rely=0.7,
                anchor=CENTER)
            loca2 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            loca2.place(relx=0.34, rely=0.7, anchor=CENTER)
            loca2.insert(10, self.fixrow(7))
            Label(
                fixroot,
                text='物業名',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.455,
                rely=0.05,
                anchor=CENTER)
            propertys = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            propertys.place(relx=0.59, rely=0.05, anchor=CENTER)
            propertys.insert(10, self.fixrow(10))
            Label(
                fixroot,
                text='期',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.45,
                rely=0.203,
                anchor=CENTER)
            qi = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            qi.place(relx=0.59, rely=0.203, anchor=CENTER)
            qi.insert(10, self.fixrow(11))
            Label(
                fixroot,
                text='座',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.45,
                rely=0.358,
                anchor=CENTER)
            build = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            build.place(relx=0.59, rely=0.358, anchor=CENTER)
            build.insert(10, self.fixrow(12))
            Label(
                fixroot,
                text='樓層',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.45,
                rely=0.513,
                anchor=CENTER)
            floor = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            floor.place(relx=0.59, rely=0.513, anchor=CENTER)
            floor.insert(10, self.fixrow(13))
            Label(
                fixroot,
                text='室號',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.45,
                rely=0.668,
                anchor=CENTER)
            room = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            room.place(relx=0.59, rely=0.668, anchor=CENTER)
            room.insert(10, self.fixrow(14))
            Label(
                fixroot,
                text='地址',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.45,
                rely=0.95,
                anchor=CENTER)
            adress = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            adress.place(relx=0.59, rely=0.95, anchor=CENTER)
            adress.insert(10, self.fixrow(9))
            Label(
                fixroot,
                text='聯繫人1',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.1,
                anchor=CENTER)
            name1 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            name1.place(relx=0.87, rely=0.1, anchor=CENTER)
            name1.insert(10, self.fixrow(17))
            Label(
                fixroot,
                text='電話1',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.25,
                anchor=CENTER)
            tel1 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            tel1.place(relx=0.87, rely=0.25, anchor=CENTER)
            tel1.insert(10, self.fixrow(18))
            Label(
                fixroot,
                text='聯繫人2',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.4,
                anchor=CENTER)
            name2 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            name2.place(relx=0.87, rely=0.4, anchor=CENTER)
            name2.insert(10, self.fixrow(19))
            Label(
                fixroot,
                text='電話2',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.55,
                anchor=CENTER)
            tel2 = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            tel2.place(relx=0.87, rely=0.55, anchor=CENTER)
            tel2.insert(10, self.fixrow(20))
            Label(
                fixroot,
                text='備註',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.7,
                anchor=CENTER)
            tip = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            tip.place(relx=0.87, rely=0.7, anchor=CENTER)
            tip.insert(10, self.fixrow(16))
            Label(
                fixroot,
                text='車位號碼',
                font=(
                    "微软雅黑",
                    8),
                fg='black',
                justify=LEFT).place(
                relx=0.46,
                rely=0.823,
                anchor=CENTER)
            carnum = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            carnum.place(relx=0.59, rely=0.823, anchor=CENTER)
            carnum.insert(10, self.fixrow(15))
            Label(
                fixroot,
                text='間隔',
                font=(
                    "微软雅黑",
                    10),
                fg='black',
                justify=LEFT).place(
                relx=0.73,
                rely=0.85,
                anchor=CENTER)
            jiange = Entry(fixroot, font=("微软雅黑", 10), fg='#04a89f')
            jiange.place(relx=0.87, rely=0.85, anchor=CENTER)
            jiange.insert(10, self.fixrow(27))
            button = Button(
                fixroot,
                text='確認修改并導出',
                font=(
                    "微软雅黑",
                    15),
                command=self.fixpri,
                activebackground='yellow').place(
                relx=0.1,
                rely=0.9,
                anchor=CENTER)
            fixroot.bind('<Key-Return>', self.fixpri_enter)

    def addpri(self):
        t1 = time.strftime('%d/%m/20%y', time.localtime(time.time()))
        t = time.strftime('%m-%d', time.localtime(time.time()))
        frow = [
            t1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None]
        frow[1] = source.get()
        frow[2] = sta.get()
        frow[3] = rentmy.get()
        frow[4] = price.get()
        frow[5] = area1.get()
        frow[6] = area2.get()
        frow[8] = loca.get()
        frow[7] = loca2.get()
        frow[9] = adress.get()
        frow[10] = propertys.get()
        frow[11] = qi.get()
        frow[12] = build.get()
        frow[13] = floor.get()
        frow[14] = room.get()
        frow[15] = carnum.get()
        frow[16] = tip.get()
        frow[17] = name1.get()
        frow[18] = tel1.get()
        frow[19] = name2.get()
        frow[20] = tel2.get()
        frow[23] = usage.get()
        frow[24] = status.get()
        frow[27] = jiange.get()
        adroot.destroy()
        p = pripath.get()
        if p == '桌面':
            path = os.path.join(
                os.path.expanduser("~"),
                'Desktop') + '/报纸%s.xlsx' % t
        else:
            path = p + '/报纸%s.xlsx' % t
        exi = os.path.exists(path)
        if exi:
            df = pd.read_excel(path)
            df1 = df.values.tolist()
            df1.append(frow)
            df = pd.DataFrame(df1, columns=self.columns)
        else:
            df = pd.DataFrame([frow], columns=self.columns)
        try:
            df.to_excel(path, index=None)
            self.show('添加完成！')
        except PermissionError:
            self.show('文件被占用，请重试')

    def fixpri(self):
        t1 = time.strftime('%d/%m/20%y', time.localtime(time.time()))
        t = time.strftime('%m-%d', time.localtime(time.time()))
        frow = [
            t1,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None]
        frow[1] = source.get()
        frow[2] = sta.get()
        frow[3] = rentmy.get()
        frow[4] = price.get()
        frow[5] = area1.get()
        frow[6] = area2.get()
        frow[7] = loca2.get()
        frow[8] = loca.get()
        frow[9] = adress.get()
        frow[10] = propertys.get()
        frow[11] = qi.get()
        frow[12] = build.get()
        frow[13] = floor.get()
        frow[14] = room.get()
        frow[15] = carnum.get()
        frow[16] = tip.get()
        frow[17] = name1.get()
        frow[18] = tel1.get()
        frow[19] = name2.get()
        frow[20] = tel2.get()
        frow[23] = usage.get()
        frow[24] = status.get()
        frow[27] = jiange.get()
        fixroot.destroy()
        p = pripath.get()
        if p == '桌面':
            path = os.path.join(
                os.path.expanduser("~"),
                'Desktop') + '/报纸%s.xlsx' % t
        else:
            path = p + '/报纸%s.xlsx' % t
        exi = os.path.exists(path)
        if exi:
            df = pd.read_excel(path)
            df1 = df.values.tolist()
            df1.append(frow)
            df = pd.DataFrame(df1, columns=self.columns)
        else:
            df = pd.DataFrame([frow], columns=self.columns)
        try:
            df.to_excel(path, index=None)
            self.show('添加完成！')
        except PermissionError:
            self.show('文件被占用，请重试')

    def revalue(self, has):
        ks = {
            1: ['星島', '經濟', '東方'],
            2: ['租', '售', '租售'],
            3: ['住宅', '工廈', '商舖', '寫字樓', '車位', '土地'],
            4: ['業主', '代理']
        }
        gek = ks.get(has)
        if has == 1:
            try:
                a = gek.index(row[1])
            except Exception as e:
                a = 0
        elif has == 2:
            try:
                a = gek.index(row[2])
            except Exception as e:
                a = 0
        elif has == 3:
            try:
                a = gek.index(row[23])
            except Exception as e:
                a = 0
        elif has == 4:
            try:
                a = gek.index(row[24])
            except Exception as e:
                a = 0
        return a

    def pri(self):
        t = time.strftime('%m-%d', time.localtime(time.time()))
        if row is None:
            self.show('先查詢詳細才能導出')
        else:
            t1 = time.strftime('%d/%m/20%y', time.localtime(time.time()))
            row[0] = t1
            row[26] = ''
            p = pripath.get()
            if p == '桌面':
                path = os.path.join(
                    os.path.expanduser("~"),
                    'Desktop') + '/报纸%s.xlsx' % t
            else:
                path = p + '/报纸%s.xlsx' % t
            exi = os.path.exists(path)
            if exi:
                df = pd.read_excel(path)
                df1 = df.values.tolist()
                df1.append(row)
                df = pd.DataFrame(df1, columns=self.columns)
            else:
                df = pd.DataFrame([row], columns=self.columns)
            try:
                df.to_excel(path, index=None)
                self.show('添加完成！')
            except PermissionError:
                self.show('文件被占用，请重试')

    def fixrow(self, i):
        r = row[i]
        if r != r:
            r = ""
        return r

    def waitroot(self):
        global waits
        waits = Tk()
        waits.title('登錄')
        photo1 = tk.PhotoImage(file='111.gif')
        i1 = Label(waits, image=photo1)
        i1.pack()
        photo2 = tk.PhotoImage(file=r'222.gif')
        i2 = Label(waits, image=photo2)

        i2.place(relx=0.1, rely=0.57)
        waits.geometry('420x290+750+300')
        name = Entry(waits, font=("微软雅黑", 10), fg='black')
        name.place(relx=0.3, rely=0.6)
        name.insert(0, 'success101')
        pasw = Entry(waits, font=("微软雅黑", 10), fg='black', show="*")
        pasw.place(relx=0.3, rely=0.69)
        pasw.insert(0, '********')
        button = Button(
            waits,
            text='            載入            ',
            font=(
                "微软雅黑",
                12),
            command=self.read,
            bg='#76BCFF')

        button.place(relx=0.295, rely=0.87)
        w = Checkbutton(waits, text='記住密碼')
        w.place(relx=0.3, rely=0.77)
        w.select()
        s = Checkbutton(waits, text='自動登錄')
        s.place(relx=0.5, rely=0.77)
        button = Button(
            waits,
            text='註冊賬號',
            font=(
                "微软雅黑",
                8),
            command=self.game,
            bg='#76BCFF')
        button.place(relx=0.7, rely=0.59)
        button = Button(
            waits,
            text='忘記密碼',
            font=(
                "微软雅黑",
                8),
            command=self.game,
            bg='#76BCFF')
        button.place(relx=0.7, rely=0.68)
        waits.bind('<Key-Return>', self.read_enter)
        waits.mainloop()

    def game(self):
        showerror('錯誤', '不存在的~')

    def warming(self,information):
        showerror('錯誤', information)

    def writloca2(self):
        lo = loca.get()
        if lo == "":
            self.warming('請輸入值再填充')
        else:
            loc = self.dic.get(lo)
            loca2.select_clear()
            loca2.insert(0, loc)

    def openxlsx(self):
        t = time.strftime('%m-%d', time.localtime(time.time()))
        p = pripath.get()
        if p == '桌面':
            path = os.path.join(
                os.path.expanduser("~"),
                'Desktop') + '/报纸%s.xlsx' % t
        else:
            path = p + '/报纸%s.xlsx' % t
        exi = os.path.exists(path)
        if exi:
            os.startfile(path)
        else:
            self.show('文件不存在，請確認今天有錄入報紙')

    def main(self):
        global telinput, text, valueinput, row, readpath, pripath
        row = None
        root = Tk()
        root.title('报纸采集器V2.1')
        root.geometry('1024x1000+890+0')
        photo = tk.PhotoImage(file=r'333.gif')
        label = Label(root, image=photo)

        label.pack()
        Label(
            root,
            text='请输入查询电话',
            font=(
                "微软雅黑",
                15),
            fg='black',
            bg='#00A2E8',
            justify=LEFT).place(
            relx=0.2,
            rely=0.07,
            anchor=CENTER)
        telinput = Entry(root, font=("微软雅黑", 15), fg='#04a89f')
        telinput.place(relx=0.2, rely=0.1, anchor=CENTER)
        button1 = Button(
            root,
            text='查询',
            font=(
                "微软雅黑",
                15),
            command=self.select,
            activebackground='yellow')
        button1.place(relx=0.38, rely=0.1, anchor=CENTER)
        button2 = Button(
            root,
            text='新增',
            font=(
                "微软雅黑",
                15),
            command=self.addmain,
            activebackground='yellow')
        button2.place(
            relx=0.68,
            rely=0.1,
            anchor=CENTER)
        button3 = Button(
            root,
            text='查詢詳細',
            font=(
                "微软雅黑",
                15),
            command=self.copy,
            activebackground='yellow').place(
            relx=0.48,
            rely=0.1,
            anchor=CENTER)
        button4 = Button(
            root,
            text='直接導出',
            font=(
                "微软雅黑",
                15),
            command=self.pri,
            activebackground='yellow').place(
            relx=0.59,
            rely=0.1,
            anchor=CENTER)
        button5 = Button(
            root,
            text='修改',
            font=(
                "微软雅黑",
                15),
            command=self.fix,
            activebackground='yellow').place(
            relx=0.75,
            rely=0.1,
            anchor=CENTER)
        button6 = Button(
            root,
            text='退出',
            font=(
                "微软雅黑",
                15),
            command=root.destroy,
            activebackground='yellow').place(
            relx=0.75,
            rely=0.17,
            anchor=CENTER
        )
        button7 = Button(
            root,
            text='打開文件',
            font=(
                "微软雅黑",
                15),
            command=self.openxlsx,
            activebackground='yellow').place(
            relx=0.4,
            rely=0.17,
            anchor=CENTER
        )
        Label(
            root,
            text='歷史剪報路徑:',
            font=(
                "微软雅黑",
                10),
            fg='black',
            bg='#00A2E8',
            justify=LEFT).place(
            relx=0.1,
            rely=0.92,
            anchor=CENTER)
        readpath = Entry(root, font=("微软雅黑", 10), fg='#04a89f')
        readpath.place(relx=0.25, rely=0.92, anchor=CENTER)
        readpath.insert(10, '桌面')
        Label(
            root,
            text='導出文件路徑:',
            font=(
                "微软雅黑",
                10),
            fg='black',
            bg='#00A2E8',
            justify=LEFT).place(
            relx=0.1,
            rely=0.96,
            anchor=CENTER)
        root.attributes("-alpha",1)
        pripath = Entry(root, font=("微软雅黑", 10), fg='#04a89f')
        pripath.place(relx=0.25, rely=0.96, anchor=CENTER)
        pripath.insert(10, '桌面')
        Label(
            root,
            text='如需更改僅需複製文件夾路徑至輸入框,無須設置文件名。例:c:/text',
            font=(
                "幼圓",
                11),
            fg='#6E0D25',
            bg='#00A2E8',
            justify=LEFT).place(
            relx=0.6,
            rely=0.945,
            anchor=CENTER)
        text = Listbox(root, font=('微软雅黑', 12), width=85, height=30, fg="red")
        # columnspan 组件所跨越的列数
        text.place(relx=0.4, rely=0.57, anchor=CENTER)
        telinput.bind('<Key-Return>', self.select_enter)
        text.bind('<Key-Return>', self.copy_enter)
        mainloop()

    def select_enter(self, event):
        self.select()

    def copy_enter(self, event):
        self.copy()

    def addpri_enter(self, event):
        self.addpri()

    def fixpri_enter(self, event):
        self.fixpri()

    def read_enter(self, event):
        self.read()

    def run(self):
        self.waitroot()

if __name__ == '__main__':
    paper = Newspaper()
    paper.waitroot()
    # paper.read()
    # paper.main()
