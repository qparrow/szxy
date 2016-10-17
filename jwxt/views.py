# -*- coding:utf-8 -*-
import szxy
from bs4 import BeautifulSoup
from django.shortcuts import render
from jwxt.forms import login_form
from django.http import HttpResponseRedirect

	
#-----------------------------------------------------------------------------------------	
	
def login(request):
		return render(request,'login.html')
def login_error(request):
		error=u'用户名或密码错误'
		return render(request,'login.html',{'error':error})

def jwxt(request):
	s,r1=szxy.load()
	if request.method=="POST" :
		form=login_form(request.POST)
		if form.is_valid():
			forms=form.cleaned_data
			username=forms['username'].encode('utf-8')
			password=forms['password'].encode('utf-8')
			
			data={'lt':'',
			'username':username,
			'password':password,
			'_eventId':'submit',
			'useValidateCode':'0',
			'isremenberme':'0'}
			
			s,data_check = szxy.login(data,s,r1)
			if data_check != szxy.check_url:
				cx_urls=szxy.jwxt_login(data,s)
				return render(request,r'jwcx.html', {'cx_urls':cx_urls})
			else:
				return HttpResponseRedirect('/login_error/')
				
def cx_result(request):
	if request.method=='GET':
		cx_url=request.GET['cx_url']
		cx_s,cx_r=szxy.cx_form(cx_url)
		request.session['cx_s']=cx_s
		request.session['cx_post_url']=cx_url
		cx_r=str(cx_r.encode('utf-8'))
		return render(request,'result.html',{'cx_r':cx_r})
	else:	
		cx_post=request.POST
		root=request.session.get('root')
		cx_post_url=request.session.get('cx_post_url')
		cx_s=request.session.get('cx_s')
		result=cx_s.post(cx_post_url,data=cx_post).text
		soup=BeautifulSoup(result)
		soup.form['action']='/jwcx/result/'
		cx_post_result=str(soup.find_all('body')[0].encode('utf-8'))
		return render(request,'result.html',{'cx_r':cx_post_result})
		
	
		
	