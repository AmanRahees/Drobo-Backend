from django.urls import path
from core.views import *
from inventory.views import *

urlpatterns = [
    path("login", LoginAPI.as_view(), name="admin-login-api"),

    path("customers", Customer_API.as_view(), name="customers-api"),
    path("customers/<int:pk>", Customer_API.as_view(), name="customer-api"),

    path("category", Category_API.as_view(), name="categories-api"),
    path("category/<int:pk>", Category_API.as_view(), name="category-api"),

    path("brand", Brand_API.as_view(), name="brands-api"),
    path("brand/<int:pk>", Brand_API.as_view(), name="brand-api"),

    path("products", Product_API.as_view(), name="products-api"),
    path("products/<int:pk>", Product_API.as_view(), name="product-api"),

    path("variants", VARIANT_API.as_view(), name="variants-api"),
    path("variants/<int:pk>", VARIANT_API.as_view(), name="variant-api"),

    # Handler Function
    path("get-descriptors", getDescriptors, name="get-descriptors"),
    path("add-alternatives", addAlternatives, name="add-alternatives"),
    path("get-alternatives/<int:id>", getAlternatives, name="get-alternatives"),
]