from django.urls import path
from .views import *

urlpatterns = [
    path('upload', uploadFile.as_view(), name="uploadFile"),
    path('download', getFile.as_view(), name="getFile"),
    path('delete', delFile.as_view(), name="delFile"),
]