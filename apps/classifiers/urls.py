from django.urls import path
from . import views

urlpatterns = [
    path("api/inst_classes", views.inst_classes, name="api_inst_classes"),
    path("api/org_types", views.org_types, name="api_org_types"),
]
