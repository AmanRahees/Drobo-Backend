from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from contexts.serializers import *
from cart.models import *
from cart.serializers import UserCouponSerializers

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_descriptors(request):
    categories = Category.objects.all().exclude(status=False)
    category_serializer = CategorySerializers(categories, many=True)
    brands = Brands.objects.all().exclude(status=False)
    brand_serializer = BrandSerializers(brands, many=True)
    context = {
        "category": category_serializer.data,
        "brands": brand_serializer.data
    }
    return Response(context, status=HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getUserItems(request):
    curr_user = request.user
    cartItems = Cart.objects.filter(user=curr_user)
    total_amount = 0
    discount_amount = 0
    for item in cartItems:
        total_amount += item.cart_product.offer_price() * item.quantity
    total_orders = Orders.objects.filter(user=curr_user)
    activeUserCoupons = UserCoupons.objects.filter(is_active=True)
    userCoupon = {}
    if (activeUserCoupons):
        _coupon = activeUserCoupons[0]
        serializer = UserCouponSerializers(_coupon, many=False)
        userCoupon = serializer.data
        discount_amount = round((_coupon.coupon.coupon_value / 100) * total_amount)
    context = {
        "cart_counter": len(cartItems),
        "total_orders": len(total_orders),
        "total_amount": total_amount,
        "discount_amount": discount_amount,
        "active_coupon": userCoupon,
    }
    return Response(context, status=HTTP_200_OK)