from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True, null=False)
    category_image = models.ImageField(upload_to="category/")
    category_offer =  models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "CATEGORIES"
    
class Brands(models.Model):
    brand_name = models.CharField(max_length=50, unique=True, null=False)
    brand_image = models.ImageField(upload_to="brands/")
    brand_offer =  models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.brand_name
    
    class Meta:
        verbose_name_plural = "BRANDS"
    
class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True, null=False)
    slug = models.SlugField(max_length=200, unique=True)
    base_image = models.ImageField(upload_to="products/")
    description = models.TextField(default="NA")
    product_offer = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = "PRODUCTS"
    
class ProductAttributes(models.Model):
    attribute_name = models.CharField(max_length=50)
    attribute_value = models.CharField(max_length=50)

    def __str__(self):
        return f"({self.attribute_name} : {self.attribute_value})"
    
    class Meta:
        verbose_name_plural = "PRODUCT ATTRIBUTES"

class ProductVariants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_attributes = models.ManyToManyField(ProductAttributes)
    price = models.IntegerField(null=False)
    stock = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product
    
    class Meta:
        verbose_name_plural = "PRODUCT VARIANTS"
    
class ProductImages(models.Model):
    products = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_imgs/")
    default_img = models.BooleanField(default=False)
    
    def __str__(self):
        return self.products
    
    class Meta:
        verbose_name_plural = "PRODUCT IMAGES"