import threading28hse
from spider591 import Spider
import threading
import add59128
import time
from spider852 import eft
def get_week():
    a=time.localtime()
    week=str(time.strftime("%w",a))
    if week == '1':
        return 24,10
    else:
        return 12,5
def input_page():
    ip = open(r'D:/ip', 'r')
    trs = input('28hse-请输入序号：\n1.爬取默认页数(租盘12页、售盘5页)\n2.自行输入爬取页数\n591将在输入完成后自动爬取\n当前数据库IP地址为：%s,输入ip更换ip地址\n————'%ip.read())
    if trs == '1':
        rentpage = 12
        salepage = 5
        print('28hse-租盘%s页，售盘%s页' % (rentpage, salepage))
    elif trs == '2':
        rentpage = input('28hse-请输入租盘页数：')
        salepage = input('28hse-请输入售盘页数：')
        try:
            rentpage = int(rentpage)
            salepage = int(salepage)
        except ValueError as e:
            print('28hse-输入错误,请输入纯数字！')
            return input_page()
        print('28hse-租盘%s页，售盘%s页' % (rentpage, salepage))
    elif trs == 'ip' or trs == 'IP':
        changeip()
        return run()
    else:
        print('28hse-输入错误，请重新输入')
        return input_page()
    return rentpage, salepage
# if __name__ == '__main__':
def changeip():
    ip=input('请输入要更换的ip地址')
    with open(r'D:/ip', 'w') as f:
        f.write(ip)
    print('更换成功当前ip地址为%s'%ip)

def run():
    rentpage,salepage=input_page()
    # rentpage,salepage=get_week()
    # print('今天是星期%s,28hse爬取租盤%s頁，售盤%s頁'%(str(time.strftime("%w",time.localtime())),rentpage,salepage))
    # if str(time.strftime("%w",time.localtime())) == 0:
        # print('今天是週日，不運行')
    # else:
    hse28=threading28hse.Hse28(rentpage,salepage)
    spider591=Spider()
    spider852=eft()
    processing2=threading.Thread(target=hse28.run)
    processing1=threading.Thread(target=spider591.run)
    processing3=threading.Thread(target=spider852.run)
    processing1.start()
    processing2.start()
    processing3.start()
    processing1.join()
    processing2.join()
    print('852 - 尚在爬取中')
    processing3.join()
    print('即将合并……请稍等')
    add59128.add()
if __name__ == '__main__':
    run()
