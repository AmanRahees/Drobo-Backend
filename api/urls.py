from django.urls import path
from accounts.views import *
from base.views import *
from cart.views import *

urlpatterns = [
    # ACCOUNTS
    path("accounts/register", RegisterAPI.as_view(), name="register-api"),
    path("accounts/login", LoginAPI.as_view(), name="login-api"),
    path("accounts/token/refresh", TokenRefreshAPI.as_view(), name="token-refresh-api"),

    # SHOP
    path("shop/products", Shop_API.as_view(), name="shop-products-api"),
    path("shop/product/<int:pk>", ProductView_API.as_view(), name="product-view-api"),

    path("cart", Cart_API.as_view(), name="carts-api"),
    path("cart/<int:pk>", Cart_API.as_view(), name="cart-api"),
]