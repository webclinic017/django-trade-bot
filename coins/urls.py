from django.urls import path 

from .api import CoinList, coin_detail, latest_price_list, get_kline

urlpatterns = [
    #market info
    path('prices', latest_price_list),

    #graphs
    path('kline/<str:asset>/<str:date>', get_kline)
]
