from django.urls import path
from .views import *

urlpatterns = [
    path('list', getTaskList.as_view(), name="getTaskList"),
    path('new', newTask.as_view(), name="newTask"),
    path('del', delTask.as_view(), name="delTask")
]