from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("config/", include("apps.config.urls")),
    path("usermanagement/", include("apps.usermanagement.urls")),
    path("staticdata/", include("apps.staticdata.urls")),
    path("marketdata/", include("apps.marketdata.urls")),
    path("accounting/", include("apps.accounting.urls")),
]
