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
    