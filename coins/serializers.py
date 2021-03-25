from rest_framework import serializers

from .models import Coin


class CoinSerializer(serializers.ModelSerializer):
    #inputs
    name        = serializers.CharField(max_length=10)
    full_name   = serializers.CharField(max_length=100)
    icon        = serializers.ImageField(required=False)


    class Meta:
        model = Coin
        fields = ("pk", "name", "full_name", "icon")


class CoinListQuerySerializer(serializers.Serializer):
    class Meta:
        model = Coin 
        fields = ("pk", "name", "full_name", "icon")