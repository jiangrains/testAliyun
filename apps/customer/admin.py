from django.contrib import admin
from customer.models import Customer, Wechat

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
	list_display = ("name", "address")
#	list_filter = ("name",)
	search_fields = ("name",)

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Wechat)
