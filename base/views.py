from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from cart.serializers import *
from base.func import *
from base.serializers.others import BannerSerializer

# Create your views here.

class Shop_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        variants = ProductVariants.objects.all().exclude(status=False, product__status=False)
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(variants, request)
        serializer = ShopProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class ProductView_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            result = getProductData(pk)
            return Response(result, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)

class Banner_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        banners = Banners.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class Address_API(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        addresses = CustomerAddress.objects.filter(user=request.user)
        serializer = Address_Serializer(addresses, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = Address_Serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)
    
class Invoice_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            order = Orders.objects.get(pk=pk)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)