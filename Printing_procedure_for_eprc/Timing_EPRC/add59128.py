import pandas as pd
import time
import os
def add():
    t = time.strftime('%m-%d', time.localtime(time.time()))
    path1=(r'C:\Users\Administrator\Desktop\jianbao\每日\591-%s.xlsx'%t)
    path2=(r'C:\Users\Administrator\Desktop\jianbao\每日\28hse-%s.xlsx'%t)
    path3=(r'C:\Users\Administrator\Desktop\jianbao\每日\852.xlsx')
    df1=pd.read_excel(path1)
    df2=pd.read_excel(path2)
    df3 = pd.read_excel(path3)
    ndf=df1.append(df2,sort=False)
    df=ndf.append(df3,sort=False)
    df.to_excel(r'C:\Users\Administrator\Desktop\jianbao\591+28hse+852%s.xlsx'%t,index=None)
    print('已合并至jianbao文件夹')
    os.system(r'C:\Users\Administrator\Desktop\jianbao\591+28hse+852%s.xlsx'%t)
# add()
# print (time.strftime("%Y-%m-%d 00:00:00", time.localtime()))
# print(bool(1))