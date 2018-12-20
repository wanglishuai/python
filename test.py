# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: why
'''

import xlrd
import json
import os

filename=r'C:\workspace\github\test\验证.xlsx'
workbook=xlrd.open_workbook(filename)

with open('C:/workspace/github/test/dict.json','r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
print(load_dict['3']['一星'])


print(workbook.sheet_names())
sheet2 = workbook.sheet_by_index(1)
print(sheet2.name,sheet2.nrows,sheet2.ncols)
rows=sheet2.nrows
cols=sheet2.ncols

for i in range(1,rows):
    for j in range(cols):
        print (sheet2.cell_value(i,j),end=' ')
        if j == 2 :
            if sheet2.cell_value(i,j)  in load_dict['3']:
                print(sheet2.cell_value(i,j),'在字典中')
            else:
                print(sheet2.cell_value(i,j),'不在字典中')
    print()
