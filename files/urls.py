from django.urls import path
from .views import *

urlpatterns = [
    path('upload', uploadFile.as_view(), name="uploadFile"),
    path('uploadcos', uploadFile_cos.as_view(), name="uploadFile_cos"),
    path('download', getFile.as_view(), name="getFile"),
    path('delete', delFile.as_view(), name="delFile"),
    path('uploadFile_cos', uploadFile_cos.as_view(), name="uploadFile_cos"),
]