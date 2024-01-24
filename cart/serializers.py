from rest_framework import serializers
from cart.models import *
from inventory.models import *


class CartProductSerializer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    product_attributes = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    price = serializers.IntegerField()
    offer_price = serializers.IntegerField()
    max_offer = serializers.IntegerField()
    stock = serializers.IntegerField()

    class Meta:
        model = ProductVariants
        fields = ('id', 'product', 'product_attributes', 'price','offer_price', 'max_offer', 'stock', 'images')

    def get_product(self, obj):
        return {
            "id": obj.product.id,
            "product_name": obj.product.product_name,
            "slug": obj.product.slug,
            "category": obj.product.category.category_name,
            "brand": obj.product.brand.brand_name
        }
    
    def get_price(self, obj):
        return obj.price
    
    def get_offer_price(self, obj):
        return obj.offer_price()
    
    def get_max_offer(self, obj):
        return obj.max_offer()
    
    def get_stock(self, obj):
        return obj.stock
    
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

class CartSerializers(serializers.ModelSerializer):
    cart_product = CartProductSerializer()
    class Meta:
        model = Cart
        fields = "__all__"

class Address_Serializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = "__all__"

class OrderItemSerializer(serializers.ModelSerializer):
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

class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField()
    orderTracks = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = "__all__"

    def get_orderItems(self, obj):
        items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data
    
    def get_orderTracks(self, obj):
        trackings = OrderTracking.objects.filter(order=obj)
        serializer = OrderTrackingSerializer(trackings, many=True)
        return serializer.data
    
class CouponSerializers(serializers.ModelSerializer):
    class Meta:
        model = Coupons
        fields = "__all__"

class UserCouponSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    coupon = serializers.SerializerMethodField()
    class Meta:
        model = UserCoupons
        fields = "__all__"

    def get_user(self, obj):
        user = CustomUser.objects.get(id=obj.user.id)
        return user.email
    
    def get_coupon(self, obj):
        coupon = Coupons.objects.get(id=obj.coupon.id)
        serializer = CouponSerializers(coupon, many=False)
        return serializer.data