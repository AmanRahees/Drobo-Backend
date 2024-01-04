from rest_framework import serializers
from accounts.models import CustomUser

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username", "email", "is_active")