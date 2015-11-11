#-*- encoding: utf-8 -*-
from django.db import models

class BaseOrder(models.Model):

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


class BaseOrderItem(models.Model):
    
    order = models.ForeignKey(Order, related_name='items', u"Order")
    product_reference = models.CharField(max_length=255, u"Product reference")
    product_name = models.CharField(max_length=255, blank=True, u"Product name")
    product = models.ForeignKey(Product, u"Product", null=True, blank=True)
    unit_price = CurrencyField(u"Unit price")
    quantity = models.IntegerField(u"Quantity")

    class Meta(object):
        abstract = True
        app_label = 'shop'
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')    