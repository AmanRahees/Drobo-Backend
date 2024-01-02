from rest_framework import serializers
from inventory.models import Brands

class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = "__all__"