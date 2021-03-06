from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', register.as_view(), name="register"),
    path('updateUserProfile', updateUserProfile.as_view(), name="updateUserProfile"),
    path('getUserInfo', getUserInfo.as_view(), name="getUserInfo")
]
