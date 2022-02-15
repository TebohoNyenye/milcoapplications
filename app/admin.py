from django.contrib import admin
from .models import Customer
from .models import *
from .views import *
class UserProfileAdmin(admin.ModelAdmin):
    list_filters = ["is_active"]
    
admin.site.register(User)
admin.site.register(Member)
admin.site.register(Customer)
admin.site.register(Guest)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.login=aloginView
admin.site.logout=logout_view



# Register your models here.
