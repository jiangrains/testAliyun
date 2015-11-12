# -*- coding: utf-8 -*-
from django.db import models

class OrderManager(models.Manager):
    
    def create_order_object(self, cart, request):
        """
        Create an empty order object and fill it with the given cart data.
        """
        order = self.model()
        order.cart_pk = cart.pk
        order.user = cart.user
        order.status = self.model.PROCESSING  # Processing
        order.order_total = cart.total_price
        return order
    
    #one cart only for one order
    def create_from_cart(self, cart, request):
    
        # First, let's remove old orders(becase the network may send more than one request to us with a unique cart)
        self.remove_old_orders(cart)
        
        order = self.create_order_object(cart, request)
