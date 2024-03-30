from django.urls import path
from . import views
from . import examples

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    # path("raw_sql_example", examples.raw_sql_example, name="raw_sql_example"),
    # path("direct_sql_example", examples.direct_sql_example, name="direct_sql_example"),
    # path("api/identifier_types", examples.api_identifier_types, name="api_identifier_types"),
    # path("api/identifier_types/<int:id>", examples.api_identifier_type, name="api_identifier_type"),
    # path("api/crud/identifier_types", examples.IdentifierTypesCR.as_view(), name="api_crud_identifier_types"),
    # path("api/crud/identifier_types/<int:id>", examples.IndentifierTypeRUD.as_view(), name="api_crud_identifier_type"),
]
