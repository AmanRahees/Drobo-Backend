from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from cart.serializers import CartSerializers, Cart
from inventory.models import ProductVariants

# Create your views here.

class Cart_API(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cartItems = Cart.objects.filter(user=request.user)
        serializer = CartSerializers(cartItems, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request, pk):
        try:
            product = ProductVariants.objects.get(pk=pk)
            is_cart_product_exists = Cart.objects.filter(user=request.user,cart_product = product).exists()
            if is_cart_product_exists:
                cartItem = Cart.objects.get(user=request.user,cart_product = product)
                cartItem.quantity += 1
                cartItem.save()
                serializer = CartSerializers(cartItem, many=False)
                return Response(serializer.data, status=HTTP_200_OK)
            else:
                cartItem = Cart.objects.create(user=request.user,cart_product = product, quantity = 1)
                return Response(status=HTTP_201_CREATED)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
        
    def put(self, request, pk):
        try:
            data = request.data
            cartItem = Cart.objects.get(pk=pk)
            if data["action"] == "increment" and cartItem.cart_product.stock > cartItem.quantity:
                cartItem.quantity += 1
            elif data["action"] == "decrement" and cartItem.quantity > 1:
                cartItem.quantity -= 1
            cartItem.save()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk):
        try:
            cartItem = Cart.objects.get(pk=pk)
            cartItem.delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)