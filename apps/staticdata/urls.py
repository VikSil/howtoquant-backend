from django.urls import path
from . import views

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    path("api/equities/<str:ticker>", views.equities, name="api_equities_by_ticker"),
    path("api/equities", views.equities, name="api_equities"),
    path("api/identifiers/codes", views.all_identifier_codes, name="api_all_identifier_codes"),
    path("api/identifiers", views.identifiers, name="api_identifiers"),
    path("api/instruments", views.instruments, name="api_instruments"),
    path("api/organizations", views.organizations, name="api_organizations"),
]
