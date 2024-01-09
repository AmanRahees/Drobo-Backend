from rest_framework import serializers
from inventory.models import Products, ProductAttributes, ProductVariants, ProductImages
from .descriptors import CategorySerializers, BrandSerializers

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
        
    def to_representation(self, instance):
        self.fields['category'] =  CategorySerializers(read_only=True)
        self.fields['brand'] =  BrandSerializers(read_only=True)
        return super(ProductSerializers, self).to_representation(instance)
    
class AttributeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributes
        fields = "__all__"

class VariantSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductVariants
        fields = "__all__"
        
class ReadVariantSerializers(serializers.ModelSerializer):
    product = ProductSerializers(read_only=True)
    product_attributes = AttributeSerializers(many=True, read_only=True)
    class Meta:
        model = ProductVariants
        fields = "__all__"