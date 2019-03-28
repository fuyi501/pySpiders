#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 00:38:14 2019

@author: fuwenwei
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import xlrd
import xlwt
import time

def get_html(url):
    header = {
        'Host':'www.qichacha.com',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Referer':'https://m.qichacha.com/',
        'Cookie':'QCCSESSID=oh95r8ii1duf3ko3323bc3aaj7; UM_distinctid=169b02f7680cef-042849fd8209f7-36667905-13c680-169b02f76819c9; zg_did=%7B%22did%22%3A%20%22169b02f789524a-0a45b0b471f28b-36667905-13c680-169b02f7896977%22%7D; hasShow=1; _uab_collina=155343909503297105162156; acw_tc=7d412b4615534390951154817e8adab7f3efe3efc0c1c078403a69e824; CNZZDATA1254842228=1688384543-1553435769-https%253A%252F%252Fwww.baidu.com%252F%7C1553451973; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1553439095,1553452277,1553452664; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201553449578798%2C%22updated%22%3A%201553454826663%2C%22info%22%3A%201553439094942%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22a5abb687ae913499726a7e132113b3ae%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1553454827',
        'Connection':'keep-alive',
        'Cache-Control':'no-cache',
    }
    html = requests.get(url, headers=header)
    return html.text

def parser_home_html(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        companys = soup.find('section', id='searchlist').find('tbody').find_all('tr')
#        print('------------------', companys)
        company = companys[0]
#        print(company.find('a', 'ma_h1').get_text())
        company_name = company.find('a', 'ma_h1').get_text()
#        print('http://www.qichacha.com' + company.find('a', 'ma_h1')['href'])
        company_detail_url = 'http://www.qichacha.com' + company.find('a', 'ma_h1')['href']
        return company_name, company_detail_url
    except:
        print('没有查到该公司')
        return None, None

def parser_detail_html(html, name):
    basic_list = {}
    soup = BeautifulSoup(html, 'lxml')
    content = soup.find('section', id='Cominfo').find_all('table')[-1].find_all('tr')
    # 法人
    try:
        basic_list['legalPersonName'] = soup.find('a', 'bname').get_text()
    except:
        basic_list['legalPersonName'] = ''
    # 企业名
    basic_list['name'] = name
    # 企业logo
    basic_list['logo'] = soup.find('div', 'imgkuang').img['src']
    # 联系方式
    try:
        basic_list['contact'] = soup.find('div', 'content').find_all('div', 'row')[1].find('span',
                                                                                           'cvlu').span.get_text().strip()
    except:
        basic_list['contact'] = ''
 
    #官网
    try:
        basic_list['websiteList'] = soup.find('div', 'content').find_all('div', 'row')[2].find_all('span','cvlu')[-1].get_text()
    except:
        basic_list['websiteList'] =''
    # 注册资本：
    try:
        basic_list['regCapital'] = content[0].find_all('td')[1].get_text().strip()
    except:
        basic_list['regCapital'] = ''
   
    # 成立日期：
    try:
        basic_list['estiblishTime'] = content[1].find_all('td')[3].get_text().strip()
    except:
        basic_list['estiblishTime'] = ''
    # 注册号：
    try:
        basic_list['regNumber'] = content[2].find_all('td')[1].get_text().strip()
    except:
        basic_list['regNumber'] = ''
 
    # 公司类型：
    try:
        basic_list['companyOrgType'] = content[4].find_all('td')[1].get_text().strip()
    except:
        basic_list['companyOrgType'] = ''
    # 所属行业：
    try:
        basic_list['industry'] = content[4].find_all('td')[3].get_text().strip()
    except:
        basic_list['industry'] = ''
 
    # 营业期限
    try:
        basic_list['operatingPeriod'] = content[8].find_all('td')[3].get_text().strip()
    except:
        basic_list['operatingPeriod'] = ''
    # 企业地址：
    try:
        basic_list['regLocation'] = content[9].find_all('td')[1].get_text().strip().split('查看地图')[0].strip()
    except:
        basic_list['regLocation'] = ''
    # 经营范围：
    try:
        basic_list['range'] = content[-1].find_all('td')[1].get_text().strip()
    except:
        basic_list['range'] = ''
    print(basic_list)
    
    return basic_list


companys_file = 'test.xlsx'
companys = xlrd.open_workbook(filename=companys_file) # 打开文件
print(companys.sheet_names()) # 获取所有表格名字
read_sheet = companys.sheet_by_index(0) # 通过索引获取表格
print(read_sheet.name, read_sheet.nrows, read_sheet.ncols)


write_companys = xlwt.Workbook()
write_sheet = write_companys.add_sheet('公司简介',cell_overwrite_ok=True)
name_list = ['表格中的名字','查询的公司名字','经营范围','法定代表人','注册人资本','成立时间','所属行业','公司地址','营业期限']
for cc in range(0,len(name_list)):
    write_sheet.write(0,cc,name_list[cc])

none_companys = open('none_company.csv', 'w+', encoding="utf-8")

for i in range(read_sheet.nrows):
    i = i + 575
    if i == 589:
        write_companys.save('test2.xls')
        break
    company_name = read_sheet.row_values(i) # 获取行内容
    company_name = company_name[0].strip()
    print(str(i) + " 获取：" + company_name)
    try:
        url = 'https://www.qichacha.com/search?key={}'.format(quote(company_name))
        print('--------------', url)
        home_html = get_html(url)
        time.sleep(2)
        # print('-----------------------', home_html)
        com_name, detail_url = parser_home_html(home_html)
        print('--------------', com_name, detail_url)
        if com_name is not None and detail_url is not None:
            detail_html = get_html(detail_url)
            time.sleep(2)
            companyInfo = parser_detail_html(detail_html, com_name)
            
            write_sheet.write(i+1, 0, company_name) # 表格中的名字
            write_sheet.write(i+1, 1, companyInfo['name']) # 查询的公司名字
            write_sheet.write(i+1, 2, companyInfo['range']) # 经营范围
            write_sheet.write(i+1, 3, companyInfo['legalPersonName']) # 法定代表人
            write_sheet.write(i+1, 4, companyInfo['regCapital']) # 注册人资本
            write_sheet.write(i+1, 5, companyInfo['estiblishTime']) # 成立时间
            write_sheet.write(i+1, 6, companyInfo['industry']) # 所属行业
            write_sheet.write(i+1, 7, companyInfo['regLocation']) # 公司地址
            write_sheet.write(i+1, 8, companyInfo['operatingPeriod']) # 营业期限
        else:
            none_companys.write(company_name + '\n')
        if i % 50 == 0:
            write_companys.save('test' + str(i) + '.xls')
        time.sleep(3)
    except:
        none_companys.write(company_name + '\n')
        print('发生错误')
        
























