# api

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from .models import Coin
from .serializers import CoinSerializer, CoinListQuerySerializer

from crypto.managers import BinanceManager

binanceManager = BinanceManager()


class CoinList(APIView):
    """List all cryptocurrency coins."""

    @swagger_auto_schema(
        query_serializer=CoinListQuerySerializer,
        responses={200: CoinSerializer(many=True)},
        tags=['Coins'],
    )
    def get(self, request):
        queryset = Coin.objects.all()
        print(queryset)
        serializer = CoinSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="apiview post description override",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        security=[],
        tags=['Coins'],
    )
    def post(self, request):
        serializer = CoinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_id="coins_dummy", operation_description="dummy operation", tags=['Coins'])
    def patch(self, request):
        pass


#custom views, such as coin info or stock

@swagger_auto_schema(method='put', request_body=CoinSerializer, tags=['Coins'])
@swagger_auto_schema(methods=['get'], manual_parameters=[
    #openapi.Parameter('test', openapi.IN_QUERY, "test manual param", type=openapi.TYPE_BOOLEAN),
    #openapi.Parameter('test_array', openapi.IN_QUERY, "test query array arg", type=openapi.TYPE_ARRAY,
    #       items=openapi.Items(type=openapi.TYPE_STRING), required=True, collection_format='multi'),
], responses={
    200: openapi.Response('OK view ', CoinSerializer),
}, tags=['Coins'])
@api_view(['GET', 'PUT'])
def coin_detail(request, pk):
    """coin_detail fbv docstring"""
    user = get_object_or_404(Coin.objects, pk=pk)
    serializer = CoinSerializer(user)
    return Response(serializer.data)



@swagger_auto_schema(method='get',
    responses={
        200: openapi.Response('OK latest market information'),
    }, tags=['Coins']
)
@api_view(['GET'])
def latest_price_list(request):
    prices = binanceManager.get_prices()

    return Response(prices)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('asset', openapi.IN_PATH, type=openapi.TYPE_STRING,
        enum=[
            "BTCUSDT",
            "BTCETH",
            "ETHUSDT",
            "ETHBTC",
            "XRPUSDT",
            "XRPBTC",
            "XMRUSDT",
            "XMRBTC",
            "XLMUSDT",
            "XLMBTC",

        ]
    ),
    openapi.Parameter('date', openapi.IN_PATH, 'Interval Date', type=openapi.TYPE_STRING,
        enum=[
            "1 month",
            "1 day",
            "12 hours",
            "1 hour"
        ]
    ),
    openapi.Parameter('end_date', openapi.IN_QUERY, 'End Date', type=openapi.TYPE_STRING,
        enum=[
            "1 month ago",
            "1 day ago",
            "12 hours ago",
            "1 hour ago"
        ], 
        required=False,
    ),
], 

responses={
    200: openapi.Response('KLine Chart analytics data'),
    401: openapi.Response('Unauthenticated'),
}, tags=['Coins'])
@api_view(['GET'])
def get_kline(request, asset, date):

    end_date = request.query_params.get('end_date')

    history = binanceManager.get_kline_history(asset, date, end_date)
    return Response(history)
