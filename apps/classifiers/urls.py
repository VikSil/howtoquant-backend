from django.urls import path
from . import views

urlpatterns = [
    path("api/accounting_methods/names", views.accounting_method_names, name="api_accounting_method_names"),
    path("api/countries", views.countries, name="api_countries"),
    path("api/currencies", views.currencies, name="api_currencies"),
    path("api/inst_classes", views.inst_classes, name="api_inst_classes"),
    path("api/org_types", views.org_types, name="api_org_types"),
    path("api/sectors", views.sectors, name="api_sectors"),
    path("api/subsectors", views.subsectors, name="api_subsectors"),
    path("api/ticker_types", views.ticker_types, name="api_ticker_types"),
]
