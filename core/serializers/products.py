from rest_framework import serializers
from inventory.models import Products
from .descriptors import CategorySerializers, BrandSerializers

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = "__all__"
        
    def to_representation(self, instance):
        self.fields['category'] =  CategorySerializers(read_only=True)
        self.fields['brand'] =  BrandSerializers(read_only=True)
        return super(ProductSerializers, self).to_representation(instance)