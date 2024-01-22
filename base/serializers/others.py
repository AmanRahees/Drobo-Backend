from rest_framework import serializers
from inventory.models import Banners


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = "__all__"