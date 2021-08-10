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
    path('modeldetail', modeldetail.as_view(), name="AImodelDetails"),
    path('details', details.as_view(), name="details"),
    path('validate', validate().as_view(), name="validate"),
    path('modelAuthor', modelAuthor().as_view(), name="modelAuthor"),
    path('updatePublished', updatePublished().as_view(), name="updatePublished"),
    path('unlockedModel', unlockedModel().as_view(), name="unlockedModel"),
    path('incAIMusage', incAIMusage.as_view(), name="incAIMusage"),
    path('getAIMusage', getAIMusage.as_view(), name="getAIMusage"),
    path('updatemodelImage',updatemodelImage.as_view(), name = "updatemodelImage"),
    path('trainingMaterialCount', trainingMaterialCount.as_view(), name="trainingMaterialCount"),
    path('personalAImodel', personalAImodel.as_view(), name="personalAImodel"),
    path('updateAIM', updateAIM.as_view(), name='updateAIM'),
    path('personalAImodelNum', personalAImodelNum.as_view(), name="personalAImodelNum"),
    path('personalAImodelUsage', personalAImodelUsage.as_view(), name="personalAImodelUsage"),
    path('train', train.as_view(), name="train"),
    path('ttt', ttt.as_view(), name="ttt"), #测试用接口
    ]
