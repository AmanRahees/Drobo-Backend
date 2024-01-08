from rest_framework import serializers
from inventory.models import Category, Brands

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = "__all__"