from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from contexts.serializers import *
from cart.models import Cart

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
    context = {
        "cart_counter": len(cartItems),
        "total_orders": 0,
    }
    return Response(context, status=HTTP_200_OK)