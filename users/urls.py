from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('updateUserProfile', updateUserProfile.as_view(), name="updateUserProfile"),
    path('getUserInfo', getUserInfo.as_view(), name="getUserInfo"),
    path('register', register.as_view(), name="register"),
    path('forgot', forgot.as_view(), name="forgot"),
    path('changePasswd', changePasswd.as_view(), name="changePasswd"),
    path('updateUserProfileImage',updateUserProfileImage.as_view(), name = "updateUserProfileImage"),
    path('returnUsrID', returnUsrID.as_view(), name="returnUsrID"),
    path('returnUserInfo', returnUserInfo.as_view(), name="returnUserInfo"),
]
