# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''
import urllib
#import urllib2
#import chardet
import re
from collections import defaultdict

def getHtml(url):
    #print url
    urlencode = url.encode('utf-8')
    #print urlencode
    page = urllib.urlopen(urlencode)
    htmlpage = page.readlines()

    return htmlpage

#获取字典key值
def getdictkey(strdict):
    #构建正则表达式
    reg = r'href="(.+?\.php)" target'
    #编译正则表达式
    str_dict = re.compile(reg)
    #使用正则表达式规则，匹配结果
    strdic = re.findall(str_dict,strdict)
    if  strdic:
        return strdic[0]
#获取字典value 1 ，天气图片
def getdictpic(strpic):
    gif_reg = r'src="(.+?\.gif)" alt'
    gif_dict = re.compile(gif_reg)
    gifvalue = re.findall(gif_dict,strpic)
    
    if  gifvalue:
        #print gifvalue[0]
        local='D:\workspace\weather\\'+gifvalue[0][-7:-4]+'.gif'
        urllib.urlretrieve(gifvalue[0],local)
        return gifvalue[0][-7:-4]
     
        
#获取字典value 2 ，文字描述
def getdictdesc(strdesc):
    desc_reg = r'target=".+>(.*)</a></p>'
    desc_dict = re.compile(desc_reg)
    descvalue = re.findall(desc_dict,strdesc)
    if  descvalue:
        return descvalue[0]

    
html = getHtml(u'http://www.weather.com.cn/static/html/legend.shtml')
#print len(html)
#print type(html)
#print html
weather_dict = defaultdict(dict)
for i in range(0,len(html)):
     
    if (html[i].find('baike.weather.com.cn') !=-1):
        if  getdictkey(html[i]) and getdictpic(html[i]):
            #print getdictkey(html[i]), getdictpic(html[i])
            desc_reg = r'http.+view-(.*)\.php'
            desc_dict = re.compile(desc_reg)
            keydict=re.findall(desc_dict,getdictkey(html[i]))[0]
            if getdictpic(html[i]).startswith('d'):
                keydict='d'+keydict
                #print keydict
            weather_dict[keydict]['pic']=getdictpic(html[i])
        if  getdictkey(html[i]) and getdictdesc(html[i]):
            #print getdictkey(html[i]), getdictdesc(html[i])
            desc_reg = r'http.+-(.*)\.php'
            desc_dict = re.compile(desc_reg)
            #keydict= re.findall(desc_dict,getdictkey(html[i]))[0]
            weather_dict[keydict]['desc']=getdictdesc(html[i])
    if (html[i].find('right_weatherindex') !=-1):
        break


#遍历输出所有字典数据 
fh = open("D:\workspace\weather\\readme.txt", 'w+')
for key in weather_dict:
    #print weather_dict[key]['pic'],weather_dict[key]['desc']

    try:
        fh.write(weather_dict[key]['pic']+'===>'+weather_dict[key]['desc']+'\n')
    except IOError:
        print "Error: 没有找到文件或读取文件失败"
    else:
        print " 内容写入文件成功"
fh.close()








