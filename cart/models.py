from django.db import models
from accounts.models import CustomUser
from inventory.models import ProductVariants

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} -> {self.cart_product.product.product_name}"

    class Meta:
        ordering = ("-id",)
    
class CustomerAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    phone = models.BigIntegerField()
    house_name = models.CharField(max_length=1024)
    road_name = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256)
    district = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    pincode = models.CharField(max_length=6)
    type = models.CharField(max_length=100)
    default_status = models.BooleanField(default=False)

orderstatus = (
    ('Order Confirmed', 'Order Confirmed'),
    ('Shipped', 'Shipped'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Completed', 'Completed'),
    ('Order cancelled', 'Order cancelled')
)

class Orders(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256)
    phone = models.IntegerField()
    house_name = models.CharField(max_length=1024)
    road_name = models.CharField(max_length=1024, blank=True, null=True)
    city = models.CharField(max_length=256)
    district = models.CharField(max_length=256)
    state = models.CharField(max_length=256)
    pincode = models.CharField(max_length=6)
    type = models.CharField(max_length=100)
    total_price = models.IntegerField()
    payment_mode = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=200, choices=orderstatus, default='Order confirmed')
    tracking_no = models.CharField(max_length=150, null=True)
    order_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.tracking_no}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_objects")
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name="order_product")
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
 
    def __str__(self):
        return f'{self.order.order_no} - {self.order.tracking_no}'