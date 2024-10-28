from django.urls import path
from .views import DepositMoneyView,add_review


# app_name = 'transactions'
urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path('book/<int:book_id>/review/', add_review, name='add_review'),
]