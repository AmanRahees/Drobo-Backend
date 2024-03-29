from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.others import *
from core.serializers.descriptors import CategorySerializers, Category, BrandSerializers, Brands
from core.serializers.products import *
from cart.models import *

# views

class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if user.is_superadmin == True:
                refresh = RefreshToken.for_user(user)
                refresh['username'] = user.username
                refresh['role'] = user.role
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Access Denied!"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"Error": "Invalid Username or Password!"}, status=status.HTTP_400_BAD_REQUEST)

class Customer_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if not pk:
            users = CustomUser.objects.exclude(role="admin")
            serializer = CustomerSerializers(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                user = CustomUser.objects.get(pk=pk)
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.is_active = not user.is_active
            user.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class Category_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk:
            try:
                category = Category.objects.get(pk=pk)
                serializer = CategorySerializers(category, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            categories = Category.objects.all()
            serializer = CategorySerializers(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = CategorySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        try:
            data = request.data.copy()
            category = Category.objects.get(pk=pk)
            try:
                if type(data['category_image']) == str:
                    data.pop('category_image')
            except:
                pass
            serializer = CategorySerializers(category, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class Brand_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk:
            try:
                brand = Brands.objects.get(pk=pk)
                serializer = BrandSerializers(brand, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            brands = Brands.objects.all()
            serializer = BrandSerializers(brands, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = BrandSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk):
        try:
            data = request.data.copy()
            brand = Brands.objects.get(pk=pk)
            try:
                if type(data['brand_image']) == str:
                    data.pop('brand_image')
            except:
                pass
            serializer = BrandSerializers(brand, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            brand = Brands.objects.get(pk=pk)
            brand.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class Product_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk:
            try:
                product = Products.objects.get(pk=pk)
                serializer = ProductSerializers(product, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            products = Products.objects.all()
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(products, request)
            serializer = ProductSerializers(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
    def post(self, request):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            data = request.data.copy()
            product = Products.objects.get(pk=pk)
            if 'base_image' in data:
                if type(data['base_image']) == str:
                    data.pop('base_image')
            serializer = ProductSerializers(product, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try:
            for id in request.data:
                product = Products.objects.get(id=id)
                product.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class VARIANT_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk:
            try:
                product = Products.objects.get(pk=pk)
                product_serializer = ProductSerializers(product, many=False)
                varinats = ProductVariants.objects.filter(product=product)
                variants_serializer = VariantSerializers(varinats, many=True)
                data = {
                    "product": product_serializer.data,
                    "variants": variants_serializer.data,
                }
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            varinats = ProductVariants.objects.all()
            paginator = PageNumberPagination()
            result_page = paginator.paginate_queryset(varinats, request)
            serializer = VariantSerializers(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = VariantSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            variant = ProductVariants.objects.get(pk=pk)
            serializer = VariantSerializers(variant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk=None):
        if pk:
            try:
                variant = ProductVariants.objects.get(pk=pk)
                variant.delete()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                for id in request.data:
                    variant = ProductVariants.objects.get(id=id)
                    variant.delete()
                return Response(status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
class Orders_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk is None:
            orders = Orders.objects.all()
            serializer = OrderSerializers(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                order = Orders.objects.get(pk=pk)
                serializer = OrderSerializers(order, many=False)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            order = Orders.objects.get(pk=pk)
            serializer = OrderSerializers(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                orderTrack = OrderTracking.objects.create(order=order, status=order.status)
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class Coupon_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None):
        if pk:
            try:
                coupon = Coupons.objects.get(pk=pk)
                serializer = CouponSerializers(coupon, many=False)
                return Response(status=status.HTTP_404_NOT_FOUND)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            coupons = Coupons.objects.all()
            serializer = CouponSerializers(coupons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = CouponSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            coupon = Coupons.objects.get(pk=pk)
            serializer = CouponSerializers(coupon, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            coupon = Coupons.objects.get(pk=pk)
            coupon.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class Banner_API(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        banners = Banners.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = BannerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            banner = Banners.objects.get(pk=pk)
            banner.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)