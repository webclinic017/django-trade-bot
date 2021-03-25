from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .managers import BinanceManager
from .serializers import WithdrawSerializer, DepositSerializer


binanceManager = BinanceManager()

#custom views, create deposit address

@swagger_auto_schema(methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['asset'],
        properties={
            'asset': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    operation_description='create deposit endpoint ',

    responses={
            200: openapi.Response('get deposit address'),
        }, tags=['Trading']
    )
@api_view(['POST'])
def get_deposit_address(request):
    """get deposit address for trading"""

    result = binanceManager.create_deposit(request.data['asset'])
    return Response(result)



@swagger_auto_schema(methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['amount', 'asset', 'address'],
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
            'asset': openapi.Schema(type=openapi.TYPE_STRING),
            'address': openapi.Schema(type=openapi.TYPE_STRING)
        },
    ),    
    operation_description='create withdrawal endpoint for given address and balance',
   
    responses={
        200: openapi.Response('create withdraw'),
    }, tags=['Trading']
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_withdraw(request):
    """create withdraw endpoint"""
    serializer = WithdrawSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.data

        result = binanceManager.create_withdraw(data['asset'], data['address'], data['amount'])
        return Response(result)
    
    return Response(serializer.errors, status=400)



@swagger_auto_schema(methods=['GET'],
    operation_description='dummy operation for getting sub accounts ',

    responses={
            200: openapi.Response('get sub accs'),
        }, tags=['Trading']
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sub_accounts(request):
    """get trading sub accounts"""

    result = binanceManager.get_sub_accounts()
    return Response(result)

@swagger_auto_schema(methods=['GET'],
    operation_description='dummy operation for getting coin information ',

    responses={
            200: openapi.Response('get coin information '),
        }, tags=['Trading']
    )
@api_view(['GET'])
@permission_classes([])
def coin_info(request):
    """get coin information """

    result = binanceManager.get_coins_info()
    return Response(result)
