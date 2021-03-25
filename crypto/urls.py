from django.urls import path 

from .api import get_deposit_address, create_withdraw, get_sub_accounts, coin_info

urlpatterns = [
    path('deposit/', get_deposit_address, name="api_trade_deposit_create"),
    path('withdraw', create_withdraw),


    path('accounts/', get_sub_accounts),
    path('info', coin_info),
]
