#-*- encoding: utf-8 -*-
from django.db import models
from user.models import User



class BaseCart(models.Model):
    # If the user is null, that means this is used for a session
    user = models.OneToOneField(User, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True
        app_label = 'shop'
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __init__(self, *args, **kwargs):
        super(BaseCart, self).__init__(*args, **kwargs)
        
    def add_product(self, product, quantity=1, queryset=None):
        from shop.models import CartItem
        # get the last updated timestamp
        # also saves cart object if it is not saved
        self.save()        
        
        if queryset is None:
            queryset = CartItem.objects.filter(cart=self, product=product)
        item = queryset
        
        if item.exists():
            cart_item = item[0]
            cart_item.quantity = cart_item.quantity + (int)quantity
            cart_item.save()

        return cart_item



class BaseCartItem(models.Model):
    """
    This is a holder for the quantity of items in the cart and, obviously, a
    pointer to the actual Product being purchased :)
    """
    cart = models.ForeignKey(Cart, related_name="items")
    quantity = models.IntegerField()
    product = models.ForeignKey(Product)

    class Meta(object):
        abstract = True
        app_label = 'shop'
        verbose_name = _('Cart item')
        verbose_name_plural = _('Cart items')

    def __init__(self, *args, **kwargs):
        # That will hold extra fields to display to the user
        # (ex. taxes, discount)
        super(BaseCartItem, self).__init__(*args, **kwargs)



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
    
    # If the user is null, the order was created with a session
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=u"顾客")
    status = models.IntegerField(choices=STATUS_CODES, default=PROCESSING, verbose_name=u"Status")
    created = models.DateTimeField(auto_now_add=True, verbose_name=u"Create")
    modified = models.DateTimeField(auto_now=True, verbose_name=u"Updated")
    cart_pk = models.PositiveIntegerField(blank=True, null=True, verbose_name=u"Cart primary key")
    
    class Meta(object):
        abstract = True
        app_label = 'order'
        
    def __unicode__(self):
        return _('Order ID: %(id)s') % {'id': self.pk}        
        
    # when user has payed , the order is completed, so we can do the next step(ship or send to other system).    
    def is_completed(self):
        return (self.status == self.COMPLETED) or (self.status == self.SHIPPED)    


class BaseOrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name=u"Order")
    product_reference = models.CharField(max_length=255, verbose_name=u"Product reference")
    product_name = models.CharField(max_length=255, blank=True, verbose_name=u"Product name")
    product = models.ForeignKey(Product, null=True, blank=True, verbose_name=u"Product")
    quantity = models.IntegerField(verbose_name=u"Quantity")

    class Meta(object):
        abstract = True
        app_label = 'shop'
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')    
