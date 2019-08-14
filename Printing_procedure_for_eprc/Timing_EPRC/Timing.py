from __future__ import unicode_literals
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import time
import sys
import os
import spider

from eprc1 import EPRCPRI
sys.path.append(r'C:\Users\Administrator\Desktop\eprc')
sys.path.append(r'c:\programdata\anaconda3\lib\site-packages')
from wxpy import *
def send_mail(text):
    try:
        retu = True # 定义执行成功时为True
        sender = '779066442@qq.com' #发送的邮箱
        pwd = 'njdzsqdnaxqlbeee' #smtp授权码
        receiver = '779066442@qq.com' #接受者邮箱
        msg = MIMEText(text, 'plain', 'utf-8')  # 发送内容
        msg['From'] = formataddr(['EPRC列印程序', sender])  # 输入发件人在收件人列表里的昵称
        msg['To'] = formataddr(['Huang', receiver])  # 服务器处理后，输入收件人邮箱的昵称
        msg['subject'] = Header('python列印', 'utf-8')  # 输入主题,不用Header直接用字符串也行
        smtp = smtplib.SMTP_SSL('smtp.qq.com', 465)  # qq邮箱的smtp服务器端口是465
        smtp.login(sender, pwd)  # 登录账号密码，密码是qq邮箱设置-账户里的授权码
        smtp.sendmail(sender, receiver, msg.as_string())  # 发送邮件
        smtp.quit()
    except BaseException as e:
        print(e)
        retu = False # 定义执行失败时为False
    if retu:
        print('邮件发送成功...')
    else:
        print('邮件发送失败...')

# bot = None
def login_wechat():
    global bot
    bot = Bot()
    send_text()

def send_news():
    ti = time.strftime("%H:%M:%S")
    try:
        qun = bot.groups().search(u'101数据运营')[0]
        # qun = bot.friends().search(u'斌')[0]
        qun.send('自动--今日EPRC列印開始')
    except:
        print(u"失败！！")
    epr = EPRCPRI()
    epr.run()
    tis = time.strftime("%H:%M:%S")
    send_mail('自动--今日EPRC已列印完成,開始時間%s,结束时间%s' % (ti, tis))
    try:
        qun = bot.groups().search(u'101数据运营')[0]
        qun.send('自动--今日EPRC已列印完成,開始時間%s,结束时间%s' % (ti, tis))
    except:
        print('通知失敗，但是程序運行完了')
def send_text():
    global bot
    print(time)
    try:
        qun = bot.groups().search(u'101数据运营')[0]
        # qun = bot.friends().search(u'斌')[0]
        qun.send('测试信息-程序正常运行中，将于今日%s开始列印'%(times))
    except Exception as e:
        print(e)
        print('微信发送失败，请重新登录！')
        bot=Bot()
        return send_text()
def timing(times):
    print('定時程序已啟動')
    login_wechat()
    print('定时程序已开始，当前时间%s，\n请注意已开启JAVA服务'%time.strftime("%H:%M:%S"))
    while 1:
        i = time.strftime("%H:%M:00")
        t = time.strftime("%H:%M:%S")
        time.sleep(10)
        if i == times:
            print(i,'开始列印')
            send_news()
            time.sleep(60)
            print('今日列印完成 明日将继续列印')
        elif i == '08:50:00':
            epr=EPRCPRI()
            print('开始删除')
            # epr.delpdf()
            spider.run()
        elif i == '18:01:00':
            print('测试微信是否在线')
            send_text()
            time.sleep(60)
        elif times.endswith('00:00') is True:
            print('定時程序運行中……現在是%s,将于%s开始列印'%(t,times))


if __name__ == "__main__":
    times='22:30:00'
    timing(times)
    # eprcprint.start()
