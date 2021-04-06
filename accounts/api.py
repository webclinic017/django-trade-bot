# api

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.pagination import PageNumberPagination

from trade_bot.settings import SWAGGER_SETTINGS

from .models import Team, User
from .serializers import UserSerializer, UserListQuerySerializer, RegistrationSerializer, TeamListQuerySerializer, TeamSerializer

from .permissions import UnauthenticatedPost
from .managers import TeamManager

class LargeResultPagination(PageNumberPagination):
    """
    Paginator for all apis
    """
    page_size = 100000
    max_page_size = 100000
    page_size_query_param = 'page_size'


class UserList(APIView):
    """Users"""
 
    permission_classes = [IsAuthenticated|UnauthenticatedPost]

    @swagger_auto_schema(
        pagination_class=LargeResultPagination,
        query_serializer=UserListQuerySerializer,
                responses={
            200: openapi.Response('Get user list', UserSerializer(many=True)),
            401: openapi.Response('Unauthorized'),
        },

        security=[{'Basic': ['read']}, {'Bearer': ['read']}],
        tags=['Users'],
    )
    def get(self, request):
        '''User List'''
        queryset = User.objects.all()
        #print(queryset)
        paginator = LargeResultPagination()
        paginator.page_size = 5

        
        results = paginator.paginate_queryset(queryset, request)
        serializer = UserSerializer(results, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="User Registration",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        responses={
            201: openapi.Response('User Created', UserSerializer),
            400: openapi.Response('Bad Data'),
            401: openapi.Response('Unauthorized'),
        },
        security=[],
        tags=['Users'],
    )
    def post(self, request):
        '''Create user model'''
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='PATCH', request_body=UserSerializer,
    responses={
        200: openapi.Response('Updated user details', UserSerializer),
        400: openapi.Response('Bad request, probably bad data'),
        401: openapi.Response('Unauthorized'),
    },
    tags=['Users']
)
@swagger_auto_schema(methods=['GET'], 
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, "User ID", type=openapi.TYPE_INTEGER),
    ], 
    responses={
        200: openapi.Response('Fetch public user details', UserSerializer),
        400: openapi.Response('Bad request, probably malformed data'),
        401: openapi.Response('Unauthorized'),
    },
    security=[{'Basic': ['read']}, {'Bearer': ['read']}],
    tags=['Users'], 
)
@api_view(['GET', 'PATCH'])
def user_detail(request, pk):
    """user_detail: Fetch details or update user"""
    user = get_object_or_404(User.objects, pk=pk)
    if not user:
        return Response({'error': 'no such user found!'})

    serializer = UserListQuerySerializer(user)

    #check if user matches the current user
    # @TODO: add admin
    #
    if request.method == "PATCH" and request.user == user:
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data)


class TeamList(APIView):
    """Teams"""
    team_manager = TeamManager()
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        query_serializer=TeamListQuerySerializer,

        pagination_class=PageNumberPagination,
        responses={
            200: openapi.Response('Get team list', TeamSerializer(many=True)),
            401: openapi.Response('Unauthorized'),
        },

        security=[{'Basic': ['read']}, {'Bearer': ['read']}],
        tags=['Users'],
    )
    def get(self, request):
        '''Team List'''
        queryset = Team.objects.all()
        #print(queryset)
        
        serializer = TeamSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Team Creation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'public': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={
            200: openapi.Response('Team Created', TeamSerializer),
            400: openapi.Response('Bad Data'),
            401: openapi.Response('Unauthorized'),
        },
        tags=['Users'],
    )
    def post(self, request):
        '''Create team model'''
        user = request.user

        if user.team is None:
            serializer = TeamSerializer(data=request.data)
            if serializer.is_valid():
                # add user as team owner
                team = serializer.create(serializer.validated_data, user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Already in a team'}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='PATCH', request_body=TeamSerializer,
    responses={
        200: openapi.Response('Updated team details', TeamSerializer),
        400: openapi.Response('Bad request, probably bad data'),
        401: openapi.Response('Unauthorized'),
    },
    tags=['Users']
)
@swagger_auto_schema(methods=['GET'], 
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, "User ID", type=openapi.TYPE_INTEGER),
    ], 
    responses={
        200: openapi.Response('Fetch public team details', TeamSerializer),
        400: openapi.Response('Bad request, probably malformed data'),
        401: openapi.Response('Unauthorized'),
    },
    security=[{'Basic': ['read']}, {'Bearer': ['read']}],
    tags=['Users'], 
)
@api_view(['GET', 'PATCH'])
def team_detail(request, pk):
    """team_detail: Fetch details or update team"""
    user = request.user
    team = get_object_or_404(Team.objects, pk=pk)

    if not team:
        return Response({'error': 'no such team found!'})

    serializer = UserListQuerySerializer(team)

    #check if user matches the current user
    # @TODO: add admin
    #
    if request.method == "PATCH" and request.user == user:
        serializer = TeamSerializer(owner=team.owner, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.data)