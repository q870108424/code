import mudle_spider
    #爬取网页二手盘叫价盘的参数
info={
    #爬取的网站名-便于创建EXCEL
    'name':'probty',
    #要爬取的页数
    'page':10,
    #页码位置用%s代替
    'url':r'http://w22.property.hk/property_search.php?p=%s&prop=&y=3&bldg=&sizeType=&size1=&size2=&saleType=&price1=&price2=&rent1=&rent2=&room=&e=&y=&pt=&dt=&isphoto=&greenform=',
    #叫价盘Xpath路径
    'xpath':'//*[@id="proplist"]/div[1]/form/table//tr/td[last()]/div[1]/a/@href',
    #线程数
    'thread':10,
    #True为测试状态只爬取测试网址
    'test_status':False,
    #测试网址,可多个，非测试模式可忽略
    'test_url':('http://www.hkea.com.hk/pub/ListingServ?currPage=1',
                'http://www.hkea.com.hk/pub/ListingServ?currPage=2'
                )
}
    #爬取页面信息的参数
inde_info={
    #保存路径
    'path':r'C:\Users\Administrator\Desktop\经纪人爬取\测试',
    #线程数
    'thread':10,
    #True为测试状态只爬取测试网址
    'test_status':True,
    #测试网址,可多个，非测试模式可忽略
    'test_url':('http://www.hkea.com.hk/pub/ListingServ?pid=H000368697',
                'http://www.hkea.com.hk/pub/ListingServ?pid=H000368591'
                )
}
    #需要的信息
    #定义一个信息集合
index_items=mudle_spider.items()
    #定义需要的字段及内容
index_items['name']='//*[@id="property-contact"]/div[2]/table/tbody/tr[1]/td[2]/text()[1]'
index_items['tel']= '//*[@id="property-contact"]/div[2]/table/tbody/tr[2]/td[2]/b/text()'


text=mudle_spider.Spider(info,inde_info,index_items)
def run(status):
    # 1仅爬取网址
    if status == 1:
        text.run_tourl()
    # 2仅爬取网页
    elif status == 2:
        text.run_toinde()
    # 3全部爬取
    elif status == 3:
        text.run_all()

# text.run_all()

run(2)

