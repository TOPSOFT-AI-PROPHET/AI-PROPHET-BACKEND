from django.urls import path
from .views import *

urlpatterns = [
    path('list', getTaskList.as_view(), name="getTaskList"),
    path('new', newTask.as_view(), name="newTask"),
    path('del', delTask.as_view(), name="delTask"),
    path('listAIM', listAIM.as_view(), name="listAIM"),
    path('addAIM', addAIM.as_view(), name="addAIM"),
    path('delAIM', delAIM.as_view(), name="delAIM"),
    path('numTask', numTask.as_view(), name="numTask"),
    path('prediction', prediction.as_view(), name="prediction"),
    path('getAIM', getAIM.as_view(), name="getAIM"),
    path('details', details.as_view(), name="details"),
    path('validate', validate.as_view(), name="validate"),
    path('incAIMusage', incAIMusage.as_view(), name="incAIMusage"),
    path('getAIMusage', getAIMusage.as_view(), name="getAIMusage")
]

