from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .models import Task
import json

class getTaskList(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        myTask = Task.objects.filter(user_id=request.user)
        return Response(
            data={"code": 200, "message": "Bingo!", "data": json.loads(serializers.serialize("json", myTask))},
            status=HTTP_200_OK
        )

class newTask(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        pass # TODO

class delTask(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        pass # TODO
