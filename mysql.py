# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''

import pymysql
import urllib3
import json

def get_bss_vm_config(url):
    http = urllib3.PoolManager()
    header={'Content-Type':'application/json'}
    fields = url
    resp = http.request('POST','http://192.168.117.169:9091/Cloud-interface/dci/bss/queryHeyingVpcDetailInfo',body=fields,headers=header)
    vmlist=json.loads(resp.data)
    print(type(vmlist))
    print(vmlist['vmList'])


def pro_bss_vm_config(PRO_INST_ID):
    sql = """
    select  concat('{"custCode":"',cus_code,'","regionId":"',YUN_RESPOOL_ID_A,'","vpcIdList":["',VPC_ID_A,'"]}'),
    concat('{"accountId":"',cloud_cust.custId,'","regionId":"',YUN_RESPOOL_ID_A,'", "vpcId":"',VPC_ID_A,'"}')
    from  rs_busi_circuit  left join cloud_cust on rs_busi_circuit.cus_code = cloud_cust.custcode
    where PRO_INST_ID='"""+PRO_INST_ID+"""'
    """
    try:
    # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        results = cursor.fetchone()
        print("专线信息： %s ,调用BSS参数：%s" % (PRO_INST_ID,results[0]))
        get_bss_vm_config(results[1])

    except:
        print ("Error: unable to fetch data")



def pro_vm_config(PRO_INST_ID):
    sql = """
    SELECT distinct RBC.PRO_INST_ID,RBC.YUN_RESPOOL_ID_A AS regionId,RBC.VPC_ID_A AS vpc_id,VM.VM_UUID AS vmID ,VMC.ALL_STORE_SPACE_MB
    FROM RS_BUSI_CIRCUIT RBC ,RS_VPC VPC ,RS_VPC_VM_RELATE VVR ,RS_VM VM,RS_VM_CONFIG VMC
    WHERE RBC.VPC_ID_A = VPC.EX_ID AND VPC.ID=VVR.VPC_ID AND VVR.STATE='10A' AND VVR.VM_ID=VM.ID AND VM.ID=VMC.VM_ID
    AND RBC.PRO_INST_ID='"""+PRO_INST_ID+"""'
    """
    try:
    # 使用 execute()  方法执行 SQL 查询
        cursor.execute(sql)
        results = cursor.fetchall()
        print ("该专线下有vm数量： %d" % (len(results)))
        for row in results:
            print ("专线信息： %s, 资源池: %s,VPCID: %s,主机ID: %s" % (row[0],row[1],row[2],row[3]))
    except:
        print ("Error: unable to fetch data")





# 打开数据库连接
rm_db = pymysql.connect("localhost","yundiao","ZTE_s0ft","cloud_rm",23306 )

# 使用 cursor() 方法创建一个游标对象 cursor

cursor = rm_db.cursor()

sql = """select cloud_cust.custid,rs_busi_circuit.CTYUN_ACCNBR,rs_busi_circuit.CTYUN_REG_EMAIL,basic_data_list.value,
rs_busi_circuit.vpn_link_code,rs_busi_circuit.work_type,rs_busi_circuit.PRO_INST_ID,
rs_busi_circuit.vpc_id_a,rs_busi_circuit.YUN_RESPOOL_ID_A,rs_busi_circuit.order_id
from rs_busi_circuit left join basic_data_list
on rs_busi_circuit.state  = basic_data_list.code and basic_data_list.TYPE_CODE ='BUSI_CIR_STATE'
left join cloud_cust on rs_busi_circuit.cus_code = cloud_cust.custCode
where ORDER_SOURCE ='Jsqxxywpt'
order by rs_busi_circuit.ACCOUNT_ID,rs_busi_circuit.CTYUN_ACCNBR,rs_busi_circuit.CTYUN_REG_EMAIL,basic_data_list.code
limit 5
"""
try:
# 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        print ("专线信息： %s, 开通状态: %s" % (row[4],row[3]))
        pro_vm_config(row[4])
        pro_bss_vm_config(row[4])
except:
    print ("Error: unable to fetch data")

# 关闭数据库连接
rm_db.close()
