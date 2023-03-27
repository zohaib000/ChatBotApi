from django.contrib.auth.models import User
from pkgutil import get_data
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .serializers import *
from rest_framework.decorators import APIView
from rest_framework.response import Response
from django.views import View
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import *

# Create your views here.
# Generate Token Manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class getData(APIView):
    def get(self, request):
        data = Data.objects.get(id=1)
        seria = DataSerializer(data)
        return Response(seria.data, status=status.HTTP_200_OK)


class putData(APIView):
    def post(self, request):
        seria = DataSerializer(data=request.data)
        if (seria.is_valid()):
            seria.save()
            return Response({'msg': 'Data has been saved !'}, status=status.HTTP_201_CREATED)


class UserRegistrationView(APIView):
    def post(self, request):
        seria = UserRegistrationSerializer(data=request.data)
        if (seria.is_valid()):
            user = seria.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Account created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Email already Exists.Try another Email!'}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        seria = UserLoginSerializer(data=request.data)
        if (seria.is_valid()):
            email = seria.data.get('email')
            pas = seria.data.get('password')
            user = authenticate(email=email, password=pas)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Logged in successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid Username or Password'}, status=status.HTTP_404_NOT_FOUND)

        return Response(seria.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seria = UserProfileSerializer(request.user)
        return Response(seria.data, status=status.HTTP_200_OK)
