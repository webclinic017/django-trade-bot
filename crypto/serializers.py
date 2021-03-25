from rest_framework import serializers

class DepositSerializer(serializers.Serializer):
    asset = serializers.CharField()
    
class WithdrawSerializer(serializers.Serializer):
    asset = serializers.CharField()
    amount = serializers.FloatField()
    address = serializers.CharField()
