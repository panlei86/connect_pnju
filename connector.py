#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import sys
import time
import cookielib
import httplib
import re
import os
from captcha import Captcha, PortalCaptcha, BrasCaptcha

reload(sys)
sys.setdefaultencoding('utf-8')

class connector:
        username = ''
        password = ''

	def __init__(self,username,password):
		self.username = username
		self.password = password
		
	def login_pnju(self):
		posturl = 'http://p.nju.edu.cn/portal.do'
		cj = cookielib.LWPCookieJar() 
		cookie_support = urllib2.HTTPCookieProcessor(cj) 
		opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
		urllib2.install_opener(opener) 
		result = urllib2.urlopen(posturl)
		text = result.read()
		code = '0'
		# 读取验证码
		try:
                        req_img = urllib2.Request('http://p.nju.edu.cn/img.html')
                        res_img = urllib2.urlopen(req_img)
                        img = res_img.read()
                        f = open('code.jpg', 'wb')
                        f.write(img)
                        f.close()
                        # 验证码识别
                        code = Captcha.Recognize('code.jpg')
                        print 'code='+code
		except:
                        pass
		
		# submit login
                posturl = 'http://p.nju.edu.cn/portal.do?action=login&url=http%3A%2F%2Fp.nju.edu.cn&p_login=p_login&username='+self.username+'&password='+self.password+'&code='+code+'&x=48&y=13'
                request = urllib2.Request(posturl)
                #print 'login...code:' + code
                response = urllib2.urlopen(request) 		
                text = response.read()
                content = text.decode('utf8')
                # 判断是否登录成功
                if content.find('验证码错误')>-1:
                        print 'captcha error'
                else:
                        print 'login p.nju success'
                request = urllib2.Request('http://p.nju.edu.cn/portal.do')
		response = urllib2.urlopen(request)
                #print urllib2.urlopen(request).read().decode('utf8')

	def logout_bras(self):
                #request = urllib2.Request('http://p.nju.edu.cn/portal.do?action=logout')
		#urllib2.urlopen(request)
		#print 'logout p.nju'
		
		posturl = 'http://bras.nju.edu.cn/selfservice/auth.html'
		cj = cookielib.LWPCookieJar() 
		cookie_support = urllib2.HTTPCookieProcessor(cj) 
		opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler) 
		urllib2.install_opener(opener) 
		urllib2.urlopen(posturl)
		
                req_img = urllib2.Request('http://bras.nju.edu.cn/selfservice/img.html?0.0826044527348131')
		res_img = urllib2.urlopen(req_img)
		img = res_img.read()
		f = open('code2.jpg', 'wb')
		f.write(img)
		f.close()
		code = Captcha.Recognize('code2.jpg')
		
		headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1','Referer' : '******'} 
		postData = {'login_username' : self.username,'action':'login','login_password' : self.password,'code':code}
		postData = urllib.urlencode(postData) 
		request = urllib2.Request(posturl, postData, headers) 
		response = urllib2.urlopen(request)

		url = 'http://bras.nju.edu.cn/selfservice/?action=online'
		request = urllib2.Request(url) 
		response = urllib2.urlopen(request)
		text = response.read()
                content = text.decode('UTF-8')
                
		# 取退出必须的id
		logout_id = self.get_logoutid(content)
		url = 'http://bras.nju.edu.cn/selfservice/?action=disconnect&id='+str(logout_id)
                request = urllib2.Request(url) 
		response = urllib2.urlopen(request)
		text = response.read()
		content = text.decode('UTF-8')
		if content.find('下线成功')>-1:
                        print 'logout bras success'
                

        def get_logoutid(self,content):
                tag1 = '<tr id='
		pos1 = content.find(tag1)+12
		if pos1 == 11:
                        return -1
		pos2 = pos1+8
		logout_id = int(content[pos1:pos2])
		return logout_id

def testConn():
    try:
        conn = httplib.HTTPConnection("www.baidu.cn",timeout=5)
        try:
            conn.request("GET", "/")
            res = conn.getresponse()
            return res.status
        finally:
            if conn is not None:
                conn.close()
    except Exception, e:
        return 400

 

if __name__ == '__main__':
	# 每隔一分钟检测一次？
	print 'running...'
	con = connector('DGxxxx','xxxx')
	con.logout_bras()
    time.sleep(3)
    con.login_pnju()
    while(True):
                try:
                        status = os.system('ping www.baidu.com')
                        print time.strftime('%Y-%m-%d %X'), 'HTTP status', status
                        #ping_result = os.system('ping baidu.com')

                        if status!=0:
                                print 'U R disconnected. connecting the p.nju.edu.cn ...'
                                # p.nju和bras先下线
                                con.logout_bras()
                                # 再连p.nju
                                time.sleep(3)
                                con.login_pnju()
                        else:
                                print 'Online. To test 120s later...'
                                time.sleep(120)
                except Exception, e:
                        pass

