from django.urls import path
from accounts.views import *
from base.views import *
from cart.views import *

urlpatterns = [
    # ACCOUNTS
    path("accounts/register", RegisterAPI.as_view(), name="register-api"),
    path("accounts/verify", VerifyAPI.as_view(), name="account-verify-api"),
    path("accounts/login", LoginAPI.as_view(), name="login-api"),
    path("accounts/token/refresh", TokenRefreshAPI.as_view(), name="token-refresh-api"),

    # SHOP
    path("shop/banners", Banner_API.as_view(), name="get-banner-api"),
    path("shop/products", Shop_API.as_view(), name="shop-products-api"),
    path("shop/product/<int:pk>", ProductView_API.as_view(), name="product-view-api"),

    # PROFILE
    path("profile/address", Address_API.as_view(), name="address-api"),

    # CART
    path("cart", Cart_API.as_view(), name="carts-api"),
    path("cart/<int:pk>", Cart_API.as_view(), name="cart-api"),
    
    # COUPON
    path("profile/coupon", Coupon_API.as_view(), name="user-coupons-api"),
    path("profile/coupon/<int:pk>", Coupon_API.as_view(), name="user-coupon-api"),

    #CHECKOUT
    path("checkout/place-order", Place_Order_API.as_view(), name="place-order-api"),

    # MY ORDERS
    path("profile/my-orders", Orders_API.as_view(), name="my-orders-api"),
    path("profile/my-orders/<int:pk>", Orders_API.as_view(), name="order-view-api"),

    # Invoice
    path("invoice/<int:pk>", Invoice_API.as_view(), name="invoice-api"),
]