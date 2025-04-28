from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import SignUpSerializer, UserSerializer

unauthorized_response = openapi.Response('Unauthorized', schema=openapi.Schema(type='string'))

@swagger_auto_schema(
    method='post',
    tags=["Authentication"],
    operation_summary="Register a new user",
    request_body=SignUpSerializer,
    responses={
        201: openapi.Response('Created successfully'),
        400: openapi.Response('Bad request (validation or user exists)'),
    }
)
@api_view(['POST'])
def register(request):
    data = request.data
    user_serializer = SignUpSerializer(data=data)

    if user_serializer.is_valid():
        if not User.objects.filter(username=data['email']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                username=data['email'],
                password=make_password(data['password']),
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    tags=["User"],
    operation_summary="Get current user profile",
    responses={
        200: UserSerializer,
        401: unauthorized_response,
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@swagger_auto_schema(
    method='put',
    tags=["User"],
    operation_summary="Update user profile",
    request_body=SignUpSerializer,
    responses={
        200: UserSerializer,
        400: openapi.Response('Bad request'),
        401: unauthorized_response,
    }
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)

    if data.get('password'):
        user.password = make_password(data['password'])

    user.save()

    serializer = UserSerializer(user)
    return Response(serializer.data)

class CustomLoginView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=["Authentication"],
        operation_summary="Login and get access/refresh tokens",
        responses={
            200: openapi.Response('Tokens returned successfully'),
            401: unauthorized_response,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
