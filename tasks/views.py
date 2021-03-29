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
    def post(self, request):
        pass # TODO

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
