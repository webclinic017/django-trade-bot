from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from rest_framework.response import Response
from rest_framework import status

from .models import Team, User, Member

class TeamListQuerySerializer(serializers.Serializer):

    class Meta:
        model = Team
        fields = ("name", "description", "score", "public", "owner", "members", "date_created", "date_updated")

class TeamSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    public = serializers.BooleanField(required=True)
    score = serializers.IntegerField(read_only=True)

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="users_team_read"
    )

    def create(self, validated_data, owner):
        team = Team(validated_data)
        team.owner = owner

        member = Member()
        member.user = owner

        team.members = (member,)
        return team


    class Meta:
        model = Team
        fields = ("name", "description", "score", "public", "owner",  "members", "date_created", "date_updated")

class UserListQuerySerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ("pk", "username", "team", "date_joined")

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=35, required=False)
    last_name = serializers.CharField(max_length=35, required=False)

    username = serializers.CharField(max_length=250, read_only=True)

    date_joined = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = ("pk", "username", "team", "first_name", "last_name", "email", "team", "date_joined")

class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=250)

    class Meta: 
        model = User
        fields = ("username", "email", "password")
