from django.urls import path
from . import views

urlpatterns = [
    # Default landing page
    path("", views.index, name="index")
]
