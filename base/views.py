from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from base.func import *

# Create your views here.

class Shop_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        result = getShopProducts()
        print(result)
        return Response(result, status=HTTP_200_OK)
    
class ProductView_API(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        try:
            result = getProductData(pk)
            return Response(result, status=HTTP_200_OK)
        except:
            return Response(status=HTTP_404_NOT_FOUND)