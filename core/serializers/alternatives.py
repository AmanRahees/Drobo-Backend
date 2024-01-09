from rest_framework import serializers
from inventory.models import *

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

class _ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.CharField()
    brand = serializers.CharField()
    variants = _VariantSerializer(many=True)