# -*- coding: utf-8 -*-
from thanksbody.models_bases import BaseProduct
from thanksbody.models_bases.managers import (
    ProductManager,
    ProductStatisticsManager,
)


class Product(BaseProduct):
    objects = ProductManager()
    statistics = ProductStatisticsManager()

    class Meta(object):
        abstract = False
        app_label = u"shop"
        verbose_name = u"Product"
        verbose_name_plural = u"Products"
