from rest_framework import serializers
from inventory.models import Category, Brands

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("category_name", "category_image", "category_offer")

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ("brand_name", "brand_image", "brand_offer")