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
<<<<<<< HEAD
        print(request)
        user_id = request.user
        ai_id = request.data['ai_id']
        description = request.data['description']
        Task.objects.create(user_id = user_id, ai_id = ai_id, description = description)
=======
        user_id = request.user
        ai_id = request.data['ai_id']
        description = request.data['description']
        Task.object.create(user_id = user_id, ai_id = ai_id, description = description)
>>>>>>> 18c7cdcee7f600230fc00984ab5011174a2d402e
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
        pass # TODO

# 暂时不需要实现的接口
class delAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        pass # TODO
