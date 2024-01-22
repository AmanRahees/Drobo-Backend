from rest_framework import serializers
from accounts.models import CustomUser
from cart.models import Orders, OrderItem, Coupons
from inventory.models import Products, ProductVariants, ProductAttributes, ProductImages, Banners

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id","username", "email", "is_active")

class OrderItemSerializers(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_product(self, obj):
        product_data = {}
        product_attributes = {}
        image_data = None
        product = ProductVariants.objects.get(id=obj.product.id)
        product_imgs = ProductImages.objects.filter(products=product)
        for attr in product.product_attributes.all():
            product_attributes[attr.attribute_name] = attr.attribute_value
        for img in product_imgs:
            if img.default_img == True:
                image_data = img.image.url
        product_data['product_name'] = product.product.product_name
        product_data['price'] = product.price
        product_data['product_attributes'] = product_attributes
        product_data['image'] = image_data
        return product_data

class OrderSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    orderItems = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = "__all__"

    def get_user(self, obj):
        user = CustomUser.objects.get(id=obj.user.id)
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "gender": user.gender,
        }

    def get_orderItems(self, obj):
        items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializers(items, many=True)
        return serializer.data
    
class CouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = "__all__"