from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from rest_framework.response import Response
from rest_framework import status

from .models import Member, Team, User

class TeamListQuerySerializer(serializers.Serializer):
    class Meta:
        model = Team
        fields = ("name", "description", "score", "owner", "date_created", "date_updated")

class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    def create(self, validated_data):
        team = Team(validated_data)
        team.owner = self.owner
        return team

    class Meta:
        model = Team
        fields = ("name", "description", "score", "owner")

class UserListQuerySerializer(serializers.Serializer):
    #team = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("pk", "username", "team", "date_joined")

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250, read_only=True)
    first_name = serializers.CharField(max_length=35, required=False)
    last_name = serializers.CharField(max_length=35, required=False)
    date_joined = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = ("pk", "username", "first_name", "last_name", "email", "team", "date_joined")

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)

    class Meta: 
        model = User
        fields = ("username", "email", "password")
