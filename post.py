# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''

from urllib3 import request
data = {'bean':'kpiInfoService','method':'loadPortFlowInfo','p0':'{"beginTime":"2019-01-24 10:00:00","endTime":"2019-01-24 14:10:00","kpiIds":[320,321]}','p1':'7','p2':'NE=180002042@15','p3':'30000','p4':'opentsdb'}
test_data_urlencode = request.urlencode(data)

request.RequestMethods.urlopen
requrl = "http://192.168.117.161:9080/Cloud-web/callRemoteFunction/exec/kpiInfoService/loadPortFlowInfo"


req = urllib3.request(url = requrl,data =test_data_urlencode)
print (req)
