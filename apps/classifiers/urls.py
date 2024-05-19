from django.urls import path
from . import views

urlpatterns = [
    path("api/org_types", views.org_types, name="api_org_types"),
]
