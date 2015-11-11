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


class Order(models.Model):

	PROCESSING = 10  # New order, addresses and shipping/payment methods chosen
	CONFIRMING = 20  # The order is pending confirmation (user is on the confirm view if has)
	CONFIRMED = 30  # The order was confirmed (user is in the payment backend)
	COMPLETED = 40  # Payment backend successfully completed (shipping if has)
	SHIPPED = 50  # The order was shipped to client(the order is done
	CANCELED = 60  # The order was canceled
	
		
	STATUS_CODES = (
		(PROCESSING, _('Processing')),
		(CONFIRMING, _('Confirming')),
		(CONFIRMED, _('Confirmed')),
		(COMPLETED, _('Completed')),
		(SHIPPED, _('Shipped')),
		(CANCELED, _('Canceled')),
    )	
	
	# If the customer is null, the order was created with a session
	customer = models.ForeignKey(Customer, blank=True, null=True, verbose_name=u"顾客")
	status = models.IntegerField(choices=STATUS_CODES, default=PROCESSING, verbose_name=u"Status")
	created = models.DateTimeField(auto_now_add=True, verbose_name=u"Create")
	modified = models.DateTimeField(auto_now=True, verbose_name=u"Updated")
	
	class Meta(object):
		abstract = True
		app_label = 'order'


class OrderItem(models.Model):
	
	order = models.ForeignKey(Order, related_name='items', u"Order")
	product_reference = models.CharField(max_length=255, u"Product reference")
	product_name = models.CharField(max_length=255, blank=True, u"Product name")
	product = models.ForeignKey(Product, u"Product", null=True, blank=True)
	unit_price = CurrencyField(u"Unit price")
	quantity = models.IntegerField(u"Quantity")
	
	#line_subtotal = CurrencyField(verbose_name=_('Line subtotal'))
	#line_total = CurrencyField(verbose_name=_('Line total'))

	class Meta(object):
		abstract = True
		app_label = 'shop'
		verbose_name = _('Order item')
		verbose_name_plural = _('Order items')	











