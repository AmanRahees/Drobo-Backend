from django.urls import path
from contexts.views import *

urlpatterns = [
    path("get-descriptors", get_descriptors, name="descriptors-context"),
    path("get-user-items", getUserItems, name="useritems-context"),
]