from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from cart.serializers import CartSerializers, OrderSerializer
from cart.models import Cart, CustomerAddress, Orders, OrderItem
from inventory.models import ProductVariants
from cart.func import generateOrderIds

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
            if product.stock > 0 and product.status == True:
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
            else:
                return Response(status=HTTP_200_OK)
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
        
class Place_Order_API(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            curr_user = request.user
            cartItem = Cart.objects.filter(user=curr_user)
            total_amount = 0
            for item in cartItem:
                total_amount += item.cart_product.price * item.quantity
            address_obj = CustomerAddress.objects.get(pk=request.data['address'])
            ORDER_ID, TRACKING_NO = generateOrderIds()
            order = Orders.objects.create(
                user = curr_user,
                full_name = address_obj.full_name,
                phone = address_obj.phone,
                house_name = address_obj.house_name,
                road_name = address_obj.road_name,
                city = address_obj.city,
                district = address_obj.district,
                state = address_obj.state,
                pincode = address_obj.pincode,
                type = address_obj.type,
                total_price = total_amount,
                order_no = ORDER_ID,
                tracking_no = TRACKING_NO,
                payment_mode = request.data['payment_method'],
                payment_id = None
            )
            for item in cartItem:
                OrderItem.objects.create(
                    order = order,
                    product = item.cart_product,
                    price = item.subtotal(),
                    quantity = item.quantity
                )
                order_product = ProductVariants.objects.get(id=item.cart_product.id)
                order_product.stock -= item.quantity
                order_product.save()
            Cart.objects.filter(user=curr_user, cart_product__status=True).delete()
            return Response(status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)
        
class Orders_API(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                order = Orders.objects.get(pk=pk)
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data, status=HTTP_200_OK)
            except:
                return Response(status=HTTP_404_NOT_FOUND)
        else:
            curr_user = request.user
            orders = Orders.objects.filter(user=curr_user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=HTTP_200_OK)