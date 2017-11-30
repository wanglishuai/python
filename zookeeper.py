#!/usr/bin/python
# -*- coding: utf-8 -*-

import zookeeper  as zoo
import os

#函数开始
def zookeeper_attr(instancename,releasenode,dir):
   "函数_获取某一个属性下的参数值"
   #path="/UCMP/instances/resourceloader/0.0.1/"+eval('dir')+"/runtime.container" 
   #path="/UCMP/instances/resourceloader/0.0.1/{dir}/runtime.container" 
   path="/UCMP/instances/{instancename}/{releasenode}/{dir}/runtime.container" 
   path1=path.format(instancename=instancename,releasenode=releasenode,dir=dir)
 #  print path1
   try:
     resourceloaderpath=zoo.get(zk,path1)
   except : 
     print
     print "4===没有相关节点信息,请确认程序名称或者版本信息"
     return

   #print "resourceloaderpath 结果长度 %d " % len(resourceloaderpath)
   runtimecontainer=resourceloaderpath[0].split('\n')
   #print "runtimecontainer  结果长度 %d " % len(runtimecontainer)
   #新建一字典，存放获取到的值
   dict1={}
   #新建一个列表，对结果做处理
   items=[]
   test1=[]
   #print  len(runtimecontainer)
   for i in range(len(runtimecontainer)):
       #print "runtimecontainer的各个值为 %d: %s" % (i,runtimecontainer[i])
       len1=len(runtimecontainer[i].split('='))
       #print len1
       if ( len1 == 2 ):
          dic1=runtimecontainer[i].split('=')[0]
          value1=runtimecontainer[i].split('=')[1]
          items.append((str(dic1),str(value1)))
          #print items

   d = dict(items)
   return d 
#函数结束

#初始化zookeeper连接
zk=zoo.init("10.245.0.96:2181");
zoo.set_debug_level(zoo.LOG_LEVEL_ERROR)
#获取所有的应用
path="/UCMP/instances"
try:
 application=zoo.get_children(zk,path);
except :
 print
 print "1===没有相关节点信息,请确认程序名称或者版本信息"
 zoo.close(zk)
 os._exit(0)
applicationlist=[]
for index in range(len(application)):
    #if ( list(application[index])[-1] != '_' and list(application[index])[0] != '&'):
    if ( not ( application[index].endswith('_') or application[index].startswith('&')) ):
         applicationlist.append(application[index])
applicationlist.sort()
for index in range(len(applicationlist)):
    print "实例 %d : %s" % (index,applicationlist[index])
#存放resourceloader下的实例，数据类型为列表
instancename=raw_input("请输入集中配置上的程序名称:")
path="/UCMP/instances/{instancename}"
path1=path.format(instancename=instancename)
try:
 resourceloader_path=zoo.get_children(zk,path1);
except :
 print
 print "2===没有相关节点信息,请确认程序名称或者版本信息"
 zoo.close(zk)
 os._exit(0)
releasenodelist=[]
for index in range(len(resourceloader_path)):
    if ( not resourceloader_path[index].endswith('_') ):
             releasenodelist.append(resourceloader_path[index])

releasenodelist.sort()
for index in range(len(releasenodelist)):
    print "版本 %d : %s" % (index,releasenodelist[index])
#存放resourceloader下的实例，数据类型为列表

releasenode=raw_input("请输入集中配置上的版本号:")

path="/UCMP/instances/{instancename}/{releasenode}"
path1=path.format(instancename=instancename,releasenode=releasenode)
try:
 resourceloader_path=zoo.get_children(zk,path1);
except :
 print
 print "3===没有相关节点信息,请确认程序名称或者版本信息"
 zoo.close(zk)
 os._exit(0)


instancelist=[]
#resourceloader_path=zoo.get_children(zk,"/UCMP/instances/resourceloader/0.0.1");
#print "resourceloader 结果长度 %d " % len(resourceloader_path);
for index in range(len(resourceloader_path)):
    #if ( list(resourceloader_path[index])[-1] != '_' ): 使用字符串函数，代替使用list函数构建列表
    if ( not resourceloader_path[index].endswith('_') ):
         instancelist.append(resourceloader_path[index])
tr='='
print
print tr*62,"report start",tr*66
for index in range(len(instancelist)):
    instance = instancelist[index]
    dict1=zookeeper_attr(instancename,releasenode,instance)
    if ( dict1 != None ) :
       print "| 序号%-10d | 实例: %-20s | 运行机器: %-20s| 运行状态: %-10s | 进程启动时间: %-20s |" % (index,instance,str(dict1.get('container.nodeHost')),str(dict1.get('container.status')),str(dict1.get('container.startTime')).replace('\\',''))
print tr*62,"report   end",tr*66
print

#关闭zookeeper连接
zoo.close(zk);
