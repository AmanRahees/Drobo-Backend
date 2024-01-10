from rest_framework import serializers
from inventory.models import *

class ShopProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    product_attributes = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariants
        fields = ('id', 'product', 'product_attributes', 'price', 'stock', 'images')

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "product_name": obj.product.product_name,
            "slug": obj.product.slug,
            "description": obj.product.description,
            "category": obj.product.category.category_name,
            "brand": obj.product.brand.brand_name
        }
    
    def get_product_attributes(self, obj):
        attributes = {}
        for attribute in obj.product_attributes.all():
            attributes[attribute.attribute_name] = attribute.attribute_value
        return attributes
    
    def get_images(self, obj):
        images_data = []
        product_images = ProductImages.objects.filter(products=obj)
        for image in product_images:
            images_data.append({
                "image": image.image.url,
                "default_img": image.default_img
            })
        return images_data
    
class _AttributeSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = {}
        for key, value in instance.items():
            data[key] = value
        return data

    def to_internal_value(self, data):
        return data

class _ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()
    default_img = serializers.BooleanField(default=False)

class _VariantSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    attributes = _AttributeSerializer(many=True)
    price = serializers.IntegerField()
    stock = serializers.IntegerField()
    images = _ImageSerializer(many=True)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ["brand_name", "brand_image"]

class ProductViewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.CharField()
    brand = BrandSerializer()
    variants = _VariantSerializer(many=True)