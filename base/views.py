from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from cart.serializers import *
from base.func import *
from base.serializers.others import *

# Create your views here.

class Shop_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        variants = ProductVariants.objects.all().exclude(status=False, product__status=False)
        paginator = ProductListPagination()
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

class Profile_API(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = ProfileSerializer(user, many=False)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def put(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            serializer = ProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            print(serializer.errors)
            return Response(status=HTTP_400_BAD_REQUEST)
        except:
            return Response(status=HTTP_404_NOT_FOUND)

class Address_API(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                addresses = CustomerAddress.objects.get(pk=pk)
                serializer = Address_Serializer(addresses, many=False)
                return Response(serializer.data, status=HTTP_200_OK)
            except:
                return Response(status=HTTP_404_NOT_FOUND)
        else:
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
    
    def put(self, request, pk):
        try:
            addresses = CustomerAddress.objects.get(pk=pk)
            serializer = Address_Serializer(addresses, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=HTTP_200_OK)
            return Response(status=HTTP_400_BAD_REQUEST)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
    
class Invoice_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            order = Orders.objects.get(pk=pk)
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)