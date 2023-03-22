from django.contrib import admin
from django.urls import path, include
from home import views
from .views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name="register"),
    path('login', UserLoginView.as_view(), name="login"),
    path('profile', UserProfileView.as_view(), name="profile"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
