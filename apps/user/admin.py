from django.contrib import admin
from user.models import User, Wechat

# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ("name", "address")
#	list_filter = ("name",)
	search_fields = ("name",)

admin.site.register(User, UserAdmin)
admin.site.register(Wechat)
