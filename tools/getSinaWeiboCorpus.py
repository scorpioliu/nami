#!/usr/bin/env python

'''
getSinaWeiboCorpus.py : Collect corpus from sina weibo.
NOTE: NEED SINA WEIBO API AND PYTHON 2.x

@author: scorpioLiu, shanzhongdeyunqi@gmail.com, 2012.03.13
@version: 0.1
@license: MIT
@copyright: (c) 2012, Project Nami
'''

import weibopy

import os
import sys
import ast
import random
import platform
import time
from datetime import date

class sinaCorpusCollector():
	def __init__(self):	
		self.AppKey = '3871875726'
		self.AppSecret = '4e4d45a95614b7fa8d075014c9b9bf47'
		self.ID = 'shanzhongdeyunqi@gmail.com'
		self.key = 'liulan'
		self.tryCnt = 4
		self.statusList = ['created_at','id','text','source','favorited','truncated',
		'in_reply_to_status_id','in_reply_to_user_id','in_reply_to_screen_name','geo',
		'mid','reposts_count','comments_count','annotations','user']
		self.userList = ['id','screen_name','name','province','city','location',
		'description','url','profile_image_url','domain','gender','followers_count',
		'friends_count','statuses_count','favourites_count','created_at','following',
		'allow_all_act_msg','remark','geo_enabled','verified','allow_all_comment',
		'avatar_large','verified_reason','follow_me','online_status',
		'bi_followers_count']
		self.geoList = ["ip","longitude","latitude","city","province","city_name",
		"province_name","pinyin","more"]
		
		self.weiboID = {}
		self.blogUrl = {}
		self.curCnt = 0
		self.curDate = date.today().strftime("%Y%m%d")
		
	def login(self):
		tryCnt = 1
		while tryCnt < self.tryCnt:
			try:
				auth = weibopy.auth.OAuthHandler(self.AppKey, self.AppSecret)
				auth.setToken(self.ID, self.key)
				self.api = weibopy.API(auth)
			except Exception as e:
				print (str(tryCnt) + ' try failed, because ' + e)
				tryCnt += 1
				time.sleep(self.tryCnt)
				continue
			return True
		return False
		
	def __freshDate(self):
		if date.today().strftime("%Y%m%d") != self.curDate:
			self.curDate = date.today().strftime("%Y%m%d")
			self.curCnt = 0
	
	def __collect(self):
		self.__freshDate()
		self.curCnt += 1
		timeline = self.api.public_timeline(count=200, page=1)	
		file_name_platform = 'corpos_sina_weibo_' + self.curDate + '_platform.txt'
		f_url = open('blog_url_from_timeline.txt', 'a')
		f_platform = open(file_name_platform,'a')
		repeatCnt = 0
		for line in timeline:
			s = line.__getattribute__('text')
			p = line.__getattribute__('source')
			id = line.__getattribute__('id')
			user_status = line.__getattribute__('user')
			user_id = user_status.__getattribute__('id')
			user_name = user_status.__getattribute__('screen_name')
			user_url = user_status.__getattribute__('url')
			location = user_status.__getattribute__('location')	
			if id in self.weiboID:
				repeatCnt += 1
				continue
			self.weiboID[str(id)] = 0
			f_platform.write('[' + p.encode('gb18030') + ']\t' + 
			'[' + str(id) + ']\t' +
			'[' + str(user_id) + ']\t' +
			'[' + user_name.encode('gb18030') + ']\t' +
			'[' + location.encode('gb18030') + ']\t' +
			s.encode('gb18030') +'\n')
			if user_url not in self.blogUrl and user_url.find('http://blog.sina.com.cn') >= 0:
				f_url.write('[' + str(user_id) + ']\t' +
				'[' + user_name.encode('gb18030') + ']\t' +
				'[' + user_url.encode('gb18030') + '\n')
		print (self.curDate + ' Round ' + str(self.curCnt) + ' ' + str(repeatCnt) + ' repeat.')
		f_platform.close()
		f_url.close()
		'''
		for i in self.statusList:
			if 'annotations'== i:
				# annotations is a tuple and i do not know how to use it now
				continue
			try:
				value = line.__getattribute__(i)
				print (value)
			except:
				pass
		'''
			
	def run(self):
		while True:
			try:
				self.__collect()
			except Exception as e:
				print (e)
				print (self.curDate + ' Round ' + str(self.curCnt) + ' failed.')
			time.sleep(10*random.random()+15)
		
		
def main():
	collector = sinaCorpusCollector()
	if not collector.login():
		print ('Login weibo failed.')
		sys.exit(1)
	print ('Login weibo successfully.')
	collector.run()
			
if '__main__' == __name__:
	main()
	