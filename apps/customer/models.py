#-*- encoding: utf-8 -*-

from django.db import models

class Wechat(models.Model): 
	nick = models.CharField(u"微信号", max_length=256)
	openId = models.CharField(u"OpenID", max_length=256, blank=True)
	
	class Meta(object):
		app_label = u"customer"

	def __init__(self, nick):
		self.nick = nick
		
	def __unicode__(self):
		return self.nick

		
class Customer(models.Model): 
	name = models.CharField(u"姓名", max_length=256) 
	phonenum = models.CharField(u"手机号码", max_length=32) 
	#如果wechat为None，说明该用户尚未绑定微信 
	wechat = models.OneToOneField(Wechat, blank=True, null=True, verbose_name=u"微信号") 
	address = models.TextField(u"住址", max_length=512, blank=True)

	class Meta(object):
		app_label = u"customer"

	def __init__(self, name, phonenum, address=u""):
		self.name = name
		self.phonenum = phonenum
		self.address = address
		self.wechat = None
		
	def __unicode__(self):
		return self.name

	def bind_wechat(self, wechat_nick):
		if self.wechat is None:
			self.wechat = Wechat(wechat_nick)			
		else:
			self.wechat.nick = wechat_nick
	
	def unbind_wechat(self):
		self.wechat = None
	
	def update_base_info(self, name, phonenum, address):
		self.name = name
		self.phonenum = phonenum
		self.address = address











