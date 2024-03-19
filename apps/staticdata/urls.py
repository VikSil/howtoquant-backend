from django.urls import path
from . import views

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    path("raw_sql_example", views.raw_sql_example, name="raw_sql_example"),
    path("direct_sql_example", views.direct_sql_example, name="direct_sql_example"),
]
