from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.serializers import *
from accounts.func import sendEmailVerification

class RegisterAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        serializer = UserRegisterSerializers(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            otp = sendEmailVerification(request, user.email)
            user.otp = otp
            user.save()
            message = 'User registered successfully. Please check your Email to verify your Account.'
            return Response({'message': message}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class VerifyAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            user = CustomUser.objects.get(email=email)
            if user.otp == int(otp):
                user.is_active = True
                user.save()
                refresh = RefreshToken.for_user(user)
                refresh['username'] = user.username
                refresh['role'] = user.role
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPI(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializers

class TokenRefreshAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        refresh = request.data.get("refresh")
        if refresh:
            try:
                refresh_obj = RefreshToken(refresh)
                access_token = str(refresh_obj.access_token)
                return Response({'refresh': str(refresh), "access": access_token}, status=status.HTTP_200_OK)
            except:
                return Response({"Error": "Invalid Refresh Token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Error": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)