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
    product = serializers.SerializerMethodField()
    product_attributes = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    class Meta:
        model = ProductVariants
        fields = "__all__"

    def get_product(self, obj):
        product = Products.objects.get(id=obj.product.id)
        return product.product_name

    def get_product_attributes(self, obj):
        attributes = {}
        for attribute in obj.product_attributes.all():
            attributes[attribute.attribute_name] = attribute.attribute_value
        return attributes
    
    def get_image(self, obj):
        images_data = None
        product_images = ProductImages.objects.filter(products=obj)
        for image in product_images:
            if image.default_img == True:
                images_data = image.image.url
        return images_data