from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from core.serializers.customers import CustomerSerializers, CustomUser
from core.serializers.descriptors import CategorySerializers, Category, BrandSerializers, Brands
from core.serializers.products import *

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
            if type(data['category_image']) == str:
                data.pop('category_image')
            serializer = CategorySerializers(category, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
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
            if type(data['brand_image']) == str:
                data.pop('brand_image')
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
            serializer = ProductSerializers(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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
    def get(self, request):
        varinats = ProductVariants.objects.all()
        serializer = VariantSerializers(varinats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        
    def delete(self, request, pk):
        try:
            variant = ProductVariants.objects.get(pk=pk)
            variant.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

