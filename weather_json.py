# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''
import  urllib
import re
#from collections import defaultdict


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
    reg = r'<p style="text-align:left;">(\d+,\W+,\W+,\W+)</p>'
    #编译正则表达式
    str_dict = re.compile(reg)
    #使用正则表达式规则，匹配结果
    strdic = re.findall(str_dict,strdict)
    if  strdic:
        return strdic[0]

    
html = getHtml(u'http://cj.weather.com.cn/support/Detail.aspx?id=51837fba1b35fe0f8411b6df')



for i in range(0,len(html)):
    if (html[i].find('text-align:left') !=-1):
        #print i,'====',html[i]
        stringcode =  html[i].replace('</p>','</p>\n')
        listcode = stringcode.split('\n')
#将结果写入文件
fh = open("D:\workspace\weather\\code.txt", 'w+')
fh.write("=====中国天气网 城市代码====="+'\n')
for i in range(0,len(listcode)):
    #print listcode[i]
    code=getdictkey(listcode[i])
    if code:
        print code
        try:
            fh.write(code+'\n')
        except IOError:
            print "Error: 没有找到文件或读取文件失败"
        else:
            print "内容写入文件成功"
fh.write("=====中国天气网 城市代码====="+'\n')
fh.close()
    





