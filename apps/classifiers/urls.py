from django.urls import path
from . import views

urlpatterns = [
    path("api/countries", views.countries, name="api_countries"),
    path("api/currencies", views.currencies, name="api_currencies"),
    path("api/inst_classes", views.inst_classes, name="api_inst_classes"),
    path("api/org_types", views.org_types, name="api_org_types"),
]
