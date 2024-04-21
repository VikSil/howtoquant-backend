from django.urls import path
from . import views

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    path("api/equities/all", views.all_equities, name="api_all_equities"),
    path("api/instruments", views.instruments, name="api_instruments"),
    path("api/instruments/<str:ticker>", views.instrument_by_ticker, name="api_instrument_by_ticker"),
    path("api/identifiers/all", views.all_identifiers, name="api_all_identifiers"),
    path("api/identifiers/codes", views.all_identifier_codes, name="api_all_identifier_codes"),

]
