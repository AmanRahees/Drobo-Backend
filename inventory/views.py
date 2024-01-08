from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from inventory.models import *
from core.serializers.descriptors import CategorySerializers, BrandSerializers
from inventory.func import *

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getDescriptors(request):
    categories = Category.objects.all()
    brands = Brands.objects.all()
    category_serializer = CategorySerializers(categories, many=True)
    brand_serializer = BrandSerializers(brands, many=True)
    data = {
        "categories": category_serializer.data,
        "brands": brand_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)