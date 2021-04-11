from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core import serializers
from .models import Task,AIModel
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import numpy as np
from sklearn import *
from sklearn.tree import DecisionTreeClassifier
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier

# 获取任务列表
class getTaskList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        myTask = Task.objects.filter(user_id=request.user, is_delete=0)
        page = request.data['page']
        paginator = Paginator(myTask, 5)
        response = {}
        response['totalCount'] = paginator.count
        response['numPerPage'] = 5
        response['totalPage'] = paginator.num_pages
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:          
            tasks = paginator.page(1)
        except InvalidPage:
            return HttpResponse('cannot find the page')
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)
        
        response['pageNum'] = page
        response['list'] = json.loads(serializers.serialize("json",myTask))

        res = {}
        res['status'] = 1
        res['message'] = 'successs'
        res['data'] = response
        return JsonResponse(res)

# 添加新任务
class newTask(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        user_id = request.user
        ai_id = request.data['ai_id']
        description = request.data['description']
        Task.objects.create(user_id_id = user_id.id, ai_id_id = ai_id, description = description)
        return Response(
            data={"code" : 200, "message": "Bingo!",}
        )


# 删除任务
class delTask(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        Task.objects.filter(user_id = request.user, task_id = request.data["task_id"]).update(is_delete = 1)
        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

# AI模型列表
class listAIM(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        AIlist = AIModel.objects.all()
        # page = request.data['page']
        # paginator = Paginator(AIlist, 5)
        response = {}
        # response['totalCount'] = paginator.count
        # response['numPerPage'] = 5
        # response['totalPage'] = paginator.num_pages
        # try:
        #     tasks = paginator.page(page)
        # except PageNotAnInteger:          
        #     tasks = paginator.page(1)
        # except InvalidPage:
        #     resp = {}
        #     resp["code"] = 404
        #     resp['message'] = 'cannot find the page'
        #     return JsonResponse(resp)
        # except EmptyPage:
        #     tasks = paginator.page(paginator.num_pages)
        # response['pageNum'] = users.number
        response['list'] = json.loads(serializers.serialize("json",AIlist))

        res = {}
        res['status'] = 200
        res['message'] = 'get success'
        res['data'] = response
        return JsonResponse(res)

# 暂时不需要实现的接口
class addAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        new_model = {}
        AIModel.objects.create(ai_name = request.data['ai_name'], ai_url = request.data['ai_url'], ai_status = request.data['ai_status'],ai_description = request.data['ai_description'], ai_type = request.data['ai_type'], ai_credit = request.data['ai_credit'])
        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

# 暂时不需要实现的接口
class delAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        pass # TODO

class getAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id = request.data['ai_id'])
        res = {}
        response = AI_instance.ai_description
        res['code'] = 200
        res['message'] = 'get success'
        res['data'] = response
        return JsonResponse(res)


class prediction(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        model_instance = AIModel.objects.get(ai_id = request.data['ai_id'])
        model = load(model_instance.ai_url)
        parameters = [[]]
        for i in range(request.data['total_para']):
            parameters[0].append(request.data['data'][i]['value'])
        parameters = np.array(parameters)
        result = model.predict(parameters)

        user_id = request.user
        ai_id = request.data['ai_id']
        Task.objects.create(user_id_id = user_id.id, ai_id_id = ai_id, ai_json = request.data['data'], ai_result = int(result[0]) , status = 1)

        return Response(
            data={"code" : 200, "message": "Bingo!",}
        )

