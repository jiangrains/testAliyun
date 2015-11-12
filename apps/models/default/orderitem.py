# -*- coding: utf-8 -*-
from thanksbody.models_bases import BaseOrderItem


class OrderItem(BaseOrderItem):

    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Order item"
        verbose_name_plural = u"Order items"
