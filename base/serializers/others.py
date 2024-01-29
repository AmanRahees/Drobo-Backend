from rest_framework import serializers
from accounts.models import CustomUser
from inventory.models import Banners

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "username", "email", "gender", "phone"]

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = "__all__"