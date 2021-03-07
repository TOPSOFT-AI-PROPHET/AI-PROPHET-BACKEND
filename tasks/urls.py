from django.urls import path
from .views import *

urlpatterns = [
    path('list', getTaskList.as_view(), name="getTaskList"),
    path('new', newTask.as_view(), name="newTask"),
    path('del', delTask.as_view(), name="delTask"),
    path('listAIM', listAIM.as_view(), name="listAIM"),
    path('addAIM', addAIM.as_view(), name="addAIM"),
    path('delAIM', delAIM.as_view(), name="delAIM"),
]