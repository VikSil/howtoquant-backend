from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/prices/new", views.get_prices, name="api_get_prices"),
]
