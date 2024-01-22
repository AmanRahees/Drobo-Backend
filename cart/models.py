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
    
    def subtotal(self):
        return self.cart_product.price * self.quantity

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
    ('Delivered', 'Delivered'),
    ('Order Cancelled', 'Order Cancelled')
)

class Orders(models.Model):
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
    total_price = models.IntegerField()
    discount_price = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    payment_mode = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=200, choices=orderstatus, default='Order Confirmed')
    tracking_no = models.CharField(max_length=150, null=True)
    order_no = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.tracking_no}'
    
    class Meta:
        ordering = ("-id",)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_objects")
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE, related_name="order_product")
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=False)
 
    def __str__(self):
        return f'{self.order.order_no} - {self.order.tracking_no}'
    
class Coupons(models.Model):
    coupon_code = models.CharField(max_length=20, unique=True)
    coupon_value = models.IntegerField(default=5)
    expiration = models.DateField()

    def __str__(self):
        return f"{self.coupon_code} ({self.coupon_value})"
    
class UserCoupons(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} ({self.coupon.coupon_code})"