# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''
import urllib
import json
from collections import defaultdict
import chardet
import gzip
import StringIO

def getHtml(url):
    #print url
    urlencode = url.encode('utf-8')
    #print urlencode
    page = urllib.urlopen(urlencode)
    htmlpage = page.read()
    compressedstream = StringIO.StringIO(htmlpage)
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    htmlpage =  gzipper.read()
    return htmlpage

def getweather(code):
    url=u'http://wthrcdn.etouch.cn/weather_mini?city='+urllib.quote(code)
    #print url
    html=getHtml(url)
    #print html

    dictweather = json.loads(html)

    #print dictweather
    '''
    for key in dictweather:
        print u'=====weather report start====='
        print u'城市名称：'+dictweather[key]['city']
        print u'城市代码：'+dictweather[key]['cityid']
        print u'最低温度：'+dictweather[key]['temp1']
        print u'最高温度：'+dictweather[key]['temp2']
        print u'天气情况：'+dictweather[key]['weather']
        print u'采集时间：'+dictweather[key]['ptime']
        print u'=====weather report end====='
    '''
    print u'================weather  report ================='
    print u'城市名称：'+dictweather['data']['city']
    print u"今天日期："+dictweather['data']['forecast'][0]['date']
    print u"今日天气："+dictweather['data']['forecast'][0]['type']
    print u"最低温度："+dictweather['data']['forecast'][0]['low']
    print u"最高温度："+dictweather['data']['forecast'][0]['high']
    print u"当前风向："+dictweather['data']['forecast'][0]['fengxiang']
    print u"当前风力："+dictweather['data']['forecast'][0]['fengli'].replace('<![CDATA[','').replace(']]>','')
    print u'当前温度：'+dictweather['data']['wendu']
    print u'小贴士：'+dictweather['data']['ganmao']
    print u'================weather  report ================='
    print u'=               Bye      Bye                    ='
    print u'================weather  report ================='

#读取文件
citycode=open("D:\workspace\weather\code.txt")
citycodelist=defaultdict(dict)
while 1:
    lines = citycode.readline()
    if not lines:
        break
    else:
        codelist=lines.split(",")
        province = codelist[3].strip()
        region = codelist[2].strip()
        city = codelist[1].strip()
        code = codelist[0].strip()
        if citycodelist[province].has_key(region):
            pass
        else:
            citycodelist[province][region]={}
        #print province,region,city,code
        if  '\xef\xbb\xbf'  in  code:
            str1 = code.replace('\xef\xbb\xbf','')
            citycodelist[province][region][city]=str1
        else:
            citycodelist[province][region][city]=code
#print type(citycodelist)
#关闭文件句柄
citycode.close()

while 1:
    #第一层嵌套，选择省份
    for province in citycodelist:
        print u'%s' % province.decode('utf-8'),
    print
    provinceselected = raw_input("province select:")
    print chardet.detect(provinceselected)
    if chardet.detect(provinceselected)['encoding'] == 'utf-8':
        pass
    else:
        provinceselectedstr=provinceselected.decode('gb2312').encode('utf-8')
    #如果选择了正确的省份，则进行地市选择，否则重新选择
    if citycodelist.has_key(provinceselected):
        #第二层循环，遍历已选择省份所有的地市
        for region in citycodelist[provinceselected]:
            print u'%s' % region.decode('utf-8'),
        print
        regionselected = raw_input("region select:")
        #print citycodelist[provinceselected][regionselected]
        #break
        if chardet.detect(regionselected)['encoding'] == 'utf-8':
            pass
        else:
            regionselected=regionselected.decode('gb2312').encode('utf-8')

        if citycodelist[provinceselected].has_key(regionselected):
            for city in citycodelist[provinceselected][regionselected]:
                print u'%s' % city.decode('utf-8'),
            print
            cityselected = raw_input("city select:")
            if chardet.detect(cityselected)['encoding'] == 'utf-8':
                pass
            else:
                cityselected=cityselected.decode('gb2312').encode('utf-8')
            cityselectedcode=citycodelist[provinceselected][regionselected][cityselected]
            if citycodelist[provinceselected][regionselected].has_key(cityselected):
                getweather(cityselected)
            else:
                print u"选择的城市有误，请重新输入:"
                continue

        else:
            print u"选择的地市有误，请重新输入:"
            continue
    else:
        print u"选择的省份有误，请重新输入:"
        continue
    goon = raw_input("Do you want to leave here(Y/N):")
    if goon == 'Y':
        continue
    else:
        break
