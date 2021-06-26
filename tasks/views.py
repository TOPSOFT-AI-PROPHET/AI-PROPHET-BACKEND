from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core import serializers
from .models import Task,AIModel
from pay.models import Transaction
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count
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


class validate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        
        ai_instance = AIModel.objects.get(ai_id = request.data['ai_id'])
        if (ai_instance.ai_credit > request.user.credit):
            return Response(
            data={"code": 100},
            status=HTTP_200_OK
            )
            
        return Response(
        data={"code": 200},
        status=HTTP_200_OK
        )

        
# 统计任务数量
class numTask(APIView):
        permission_classes = (IsAuthenticated,)

        def post(self, request):
            Task_num=Task.objects.filter(is_delete = 0,user_id = request.user.id).aggregate(Task_num = Count("task_id"))
            Task_finish=Task.objects.filter(status = 100, is_delete = 0 , user_id = request.user.id).aggregate(Task_finish = Count("task_id"))

            return Response(
            data={"code": 200, "data":{"num_of_task":str(Task_num['Task_num']),"num_of_finished_tasks":str(Task_finish['Task_finish'])}},
            status=HTTP_200_OK
        )
class getAIM(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id = request.data['ai_id'])
        res = {}
        response = AI_instance.ai_description
        res['code'] = 200
        res['message'] = 'get success'
        res['data'] = json.loads(response)
        return JsonResponse(res)


class prediction(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        model_instance = AIModel.objects.get(ai_id = request.data['ai_id'])
        model = load(model_instance.ai_url)
        parameters = [[]]
        ai_json = []
        for i in range(request.data['total_para']):
            parameters[0].append(int(request.data['data'][i]['value']))
            ai_json.append({str(i):int(request.data['data'][i]['value'])})
        parameters = np.array(parameters)
        result = model.predict(parameters)

        user_id = request.user
        ai_id = request.data['ai_id']
        Task.objects.create(user_id_id = user_id.id, ai_id_id = ai_id, ai_name = model_instance.ai_name, ai_json = json.dumps(ai_json), ai_result = int(result[0]) , status = 100, description = "Under development")

        #扣费
        Transaction.objects.create(user_id = request.user,status = 1,method = 1,order = model_instance.ai_name ,credit =  model_instance.ai_credit)
        request.user.credit = request.user.credit - model_instance.ai_credit
        request.user.save()

        return Response(
            data={"code" : 200, "message": "Bingo!",}
        )

class details(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        task_id = request.data['task_id']
        task_instance = Task.objects.get(task_id = task_id)
        ai_instance = AIModel.objects.get(ai_id = task_instance.ai_id.ai_id)
        Task_description=task_instance.description
        ai_json=json.loads(task_instance.ai_json)
        ai_url=task_instance.ai_id.ai_url
        ai_result=task_instance.ai_result
        status=task_instance.status
        time_start=task_instance.time_start
        ai_credit=task_instance.ai_id.ai_credit
        ai_params=[]
        sourcedata = json.loads(ai_instance.ai_description)

        for i in range(sourcedata["total_param"]):

            ai_params.append({"para_name":sourcedata["details"][i]["name"],"para_value":ai_json[i][str(i)]})




    

        return Response(
            data={"code" : 200, "description" : str(Task_description), "ai_json" : [ai_json], "ai_url" : str(ai_url),
                "ai_result" : str(ai_result), "status" : status, "time_start" : time_start, "cost" : int(ai_credit), "ai_params" : ai_params}
        )




