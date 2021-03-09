from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core import serializers
from .models import Task
import json

# 获取任务列表
class getTaskList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        myTask = Task.objects.filter(user_id=request.user, is_delete=0)
        return Response(
            data={"code": 200, "message": "Bingo!", "data": json.loads(serializers.serialize("json", myTask))},
            status=HTTP_200_OK
        )

# 添加新任务
class newTask(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        pass # TODO

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
        pass # TODO

# 暂时不需要实现的接口
class delAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        pass # TODO
