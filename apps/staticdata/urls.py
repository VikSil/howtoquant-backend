from django.urls import path
from . import views
from . import examples

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    path("api/equities/all", views.all_equities, name="api_all_equities"),
    path("api/instruments", views.instruments, name="api_instruments"),
    path("api/instruments/<str:ticker>", views.instrument_by_ticker, name="api_instrument_by_ticker"),
    path("api/identifiers/all", views.all_identifiers, name="api_all_identifiers"),
    path("api/identifiers/codes", views.all_identifier_codes, name="api_all_identifier_codes"),
    # path("raw_sql_example", examples.raw_sql_example, name="raw_sql_example"),
    # path("direct_sql_example", examples.direct_sql_example, name="direct_sql_example"),
    # path("api/identifier_types", examples.api_identifier_types, name="api_identifier_types"),
    # path("api/identifier_types/<int:id>", examples.api_identifier_type, name="api_identifier_type"),
    # path("api/crud/identifier_types", examples.IdentifierTypesCR.as_view(), name="api_crud_identifier_types"),
    # path("api/crud/identifier_types/<int:id>", examples.IndentifierTypeRUD.as_view(), name="api_crud_identifier_type"),
]
