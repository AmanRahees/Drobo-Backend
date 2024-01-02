from django.urls import path
from accounts.views import *

urlpatterns = [
    # ACCOUNTS
    path("accounts/register", RegisterAPI.as_view(), name="register-api"),
    path("accounts/login", LoginAPI.as_view(), name="login-api"),
    path("accounts/token/refresh", TokenRefreshAPI.as_view(), name="token-refresh-api"),

    # SHOP
    
]