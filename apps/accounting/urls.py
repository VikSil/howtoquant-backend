from django.urls import path
from . import views

urlpatterns = [
    # Default landing page
    path("", views.index, name="index"),
    path("api/books", views.books, name="api_books"),
    path("api/strategies", views.strategies, name="api_strategies"),
    path("api/pbaccounts/names", views.pbaccounts_names, name="api_pbaccounts_names"),
    path("api/pbaccounts", views.pbaccounts, name="api_pbaccounts"),
    path("api/trades/<int:id>", views.trades, name="api_trades_by_id"),
    path("api/trades", views.trades, name="api_trades"),
]
