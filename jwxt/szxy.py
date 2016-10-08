# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 19:49:57 2016

@author: qinpiao
"""
import re
import requests
import threading
from bs4 import BeautifulSoup
url_root='http://i.cqut.edu.cn/'      #数字化校园地址
url='http://i.cqut.edu.cn/portal.do'  #数字化校园实际登录页地址
check_url='http://i.cqut.edu.cn/zfca/login?service=http%3A%2F%2Fi.cqut.edu.cn%2Fportal.do'
zf_url='http://i.cqut.edu.cn/zfca?yhlx=student&login=0122579031373493728&url=xs_main.aspx'#正方教务系统的地址
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
'Accept-Encoding': 'gzip, deflate'}
#------------------------------------------------------------------------------
def load():
	s=requests.Session()
	s.get(url_root,headers=headers)
	r1=s.get(url,headers=headers)
	return s,r1


#获取页面随账户和密码隐藏提交的lt值
def get_hid_input(page):
    pattern='(name="lt")(.*?)(/>)'
    pattern1='(value=")(.*?)(")'
    LT=re.findall(pattern,page,re.S)[0][1]
    lt=re.findall(pattern1,LT,re.S)[0][1]
    return lt

	

#-----------------------------------------------------------------------------
         
#登录数字化校园
def login(data,s,r1):
	data['lt']=get_hid_input(r1.text)
	s.post(r1.url,data=data,headers=headers)
	r2=s.get(r1.url,headers=headers)
	return s,r2.url

#------------------------------------------------------------------------------

#取得教务系统的信息查询项的所有链接
def zf_list(zf_page):
    soup=BeautifulSoup(zf_page)
    l=str(soup.find_all('ul',attrs={'class':'sub'})[4]) 
    zf_l=BeautifulSoup(l)
    zf_url_list=zf_l.find_all('a')
    zf_data={}
    for i in zf_url_list :
        url=BeautifulSoup(str(i)).a['href']
        s=BeautifulSoup(str(i)).a.text.strip().encode('UTF-8')
        zf_data[s]=url
    return zf_data
#---------------------------------------------------------------------------------   

#取出后面查询信息时需要的链接的一部分
def get_cx_root(zf_jw,zf_data):
	pattern=r'(.*?)(xs)'
	root=re.findall(pattern,zf_jw.url,re.S)[0][0].decode('utf-8')
	cx_urls={}
	for k in zf_data:
		cx_key=k
		url=zf_data[k]
		cx_url=root+url
		cx_urls[cx_key]=cx_url
	return cx_urls
    
    
#------------------------------------------------------------------------------   

    
'''该处提供的查询链接有：
学生个人课表，学生成绩统计，
等级考试成绩查询，培养计划，
学生成绩查询，全校总课表            
''' 
def cx_form(cx_url):
	cx_s=requests.Session()
	cx_i=cx_s.get(cx_url)
	soup=BeautifulSoup(cx_i.text)
	soup.form['action']='/jwcx/result/'
	cx_r=soup.find_all('body')[0]
	return cx_s,cx_r

   
#------------------------------------------------------------------------------
def jwxt_login(data,s):
	zf_jw=s.get(zf_url)
	zf_data=zf_list(zf_jw.text)
	cx_urls=get_cx_root(zf_jw,zf_data)
	return cx_urls
	
	'''
	cx_url=get_cx_root(zf_jw,zf_data,'学生个人课表')
	page=requests.get(cx_url,headers=headers)
	soup=BeautifulSoup(page.text)
	kb=soup.prettify('utf-8')
	return page.text
	'''







    
