from django.urls import path
from core.views import *

urlpatterns = [
    path("category", Category_API.as_view(), name="categories-api"),
    path("category/<int:pk>", Category_API.as_view(), name="category-api"),
]