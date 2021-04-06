from django.urls import path 

from .api import CoinList, coin_detail, latest_price_list, latest_future_list, get_kline

urlpatterns = [
    #market info
    path('prices', latest_price_list),
    path('futures', latest_future_list),

    #graphs
    path('kline/<str:asset>/<str:date>', get_kline)
]
