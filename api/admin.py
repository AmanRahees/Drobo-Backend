from django.contrib import admin
from accounts.models import CustomUser
from inventory.models import *
from cart.models import *

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('product_name',)}

admin.site.register(CustomUser)

admin.site.register(Category)
admin.site.register(Brands)
admin.site.register(Products, ProductAdmin)
admin.site.register(ProductAttributes)
admin.site.register(ProductVariants)
admin.site.register(ProductImages)

admin.site.register(Cart)
admin.site.register(CustomerAddress)
admin.site.register(Orders)
admin.site.register(OrderItem)