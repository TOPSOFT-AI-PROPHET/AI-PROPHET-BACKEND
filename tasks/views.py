from django.contrib.auth.models import Permission
from django.db import models
from rest_framework import response
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core import serializers
from .models import Task, AIModel
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
from rest_framework.parsers import MultiPartParser
import uuid
import sys
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from .models import UserProfile

# 获取任务列表


class getTaskList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        myTask = Task.objects.filter(user_id_id=request.user, is_delete=0)
        page = request.data['page']
        paginator = Paginator(myTask, 5)
        response = {}
        # pagination 
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
        response['list'] = json.loads(serializers.serialize("json", myTask))

        res = {}
        res['status'] = 1
        res['message'] = 'successs'
        res['data'] = response
        return JsonResponse(res)


# 添加新任务
class newTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user
        ai_id = request.data['ai_id']
        description = request.data['description']
        Task.objects.create(user_id_id = user.id, ai_id_id = ai_id, description = description)
        return Response(
            data={"code": 200, "message": "Bingo!", }
        )


# 删除任务
class delTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # we use logical deletion 
        Task.objects.filter(user_id_id = request.user, task_id = request.data["task_id"]).update(is_delete = 1)
        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

# AI模型列表


class listAIM(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AIlist = AIModel.objects.filter(ai_published = 1)
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
        response['list'] = json.loads(serializers.serialize("json", AIlist))

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
        AIModel.objects.create(ai_name=request.data['ai_name'], ai_url=request.data['ai_url'], ai_status=request.data['ai_status'],
                               ai_description=request.data['ai_description'], ai_type=request.data['ai_type'], ai_credit=request.data['ai_credit'])
        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

# 暂时不需要实现的接口


class delAIM(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        pass  # TODO

# verifie whether a user holds enough credit to run tasks
class validate(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        ai_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        if (ai_instance.ai_credit > request.user.credit):
            return Response(
                data={"code": 100},
                status=HTTP_200_OK
            )

        return Response(
            data={"code": 200},
            status=HTTP_200_OK
        )

        
# 统计现有任务数量和已完成任务数量
class numTask(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Task_num = Task.objects.filter(
            is_delete=0, user_id_id=request.user.id).aggregate(Task_num=Count("task_id"))
        Task_finish = Task.objects.filter(
            status=100, is_delete=0, user_id_id=request.user.id).aggregate(Task_finish=Count("task_id"))

        return Response(
            data={"code": 200, "data": {"num_of_task": str(
                Task_num['Task_num']), "num_of_finished_tasks": str(Task_finish['Task_finish'])}},
            status=HTTP_200_OK
        )

# get ai_model description 
class getAIM(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        response = AI_instance.ai_description
        res['code'] = 200
        res['message'] = 'get success'
        res['data'] = json.loads(response)
        return JsonResponse(res)

# return how many times does this ai_model be used 
class getAIMusage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        res['code'] = 200
        res['message'] = 'get success'
        res['data'] = AI_instance.ai_usage
        return JsonResponse(res)

# when this api be called, usage of this ai_model will plus one
class incAIMusage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        AI_instance.ai_usage = AI_instance.ai_usage + 1
        AI_instance.save()
        res = {}
        res['code'] = 200
        res['message'] = 'OK'
        return JsonResponse(res)

# call ai_model and pass in parameters which minus credit automatically 
class prediction(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        model_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        model = load(model_instance.ai_url)
        parameters = [[]]
        ai_json = []
        for i in range(request.data['total_para']):
            parameters[0].append(int(request.data['data'][i]['value']))
            ai_json.append({str(i): int(request.data['data'][i]['value'])})
        parameters = np.array(parameters)
        result = model.predict(parameters)

        user_id = request.user
        ai_id = request.data['ai_id']
        Task.objects.create(user_id_id=user_id.id, ai_id_id=ai_id, ai_name=model_instance.ai_name, ai_json=json.dumps(
            ai_json), ai_result=int(result[0]), status=100, description="Under development")

        #扣费
        Transaction.objects.create(user_id=request.user, status=1, method=1,
                                   order=model_instance.ai_name, credit=model_instance.ai_credit)
        request.user.credit = request.user.credit - model_instance.ai_credit
        request.user.save()

        return Response(
            data={"code": 200, "message": "Bingo!", }
        )

# return ai_model details 
class AImodelDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        
        if AI_instance.ai_frozen == 0:
            res['code'] = 200
            res['message'] = 'get success'
            response = json.loads(serializers.serialize("json", [AI_instance]))
            res['data'] = response
        else:
            res["code"] = 404
            res['message'] = 'cannot find the page'
        return JsonResponse(res)

# return model author 
class modelAuthor(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        AI_model = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        author = AI_model.ai_author
        publish = AI_model.ai_published
        res['code'] = 200
        res['message'] = 'get success'
        res['author'] = author
        res['publish'] = publish
        return JsonResponse(res)

# we need to connect with cos service and pass in with uuid encrypted information
class updatemodelImage(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        file_obj = request.data['modelprofile']
        aiid = request.data['ai_id']

        secret_id = 'AKIDZx60e1HAamulLgNW1MUR7WdT6UkktKp4'      # 替换为用户的 secretId
        secret_key = '7xW4KOCiyyoN4WhbDySjjSu42kiPq1vx'      # 替换为用户的 secretKey
        region = 'ap-chengdu'     # 替换为用户的 Region
        token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id,
                           SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)
        uuid_namespace = uuid.uuid3(uuid.NAMESPACE_OID, str(
            UserProfile.objects.get(id=request.user.id).id))
        uuid_str = str(uuid.uuid3(uuid_namespace, str(uuid.uuid4())))
        response = client.put_object(
            Bucket='prophetsrc-1305001068',
            Body=file_obj.read(),
            Key=uuid_str+".jpg",
            StorageClass='STANDARD',
            EnableMD5=True)
        model = AIModel.objects.get(ai_id=aiid)
        model.ai_model_profile = uuid_str
        model.save()

        return Response(
            data={"code": 200, "message": "Bingo!",
                  "ETag": response['ETag'], "uuid": uuid_str},
            status=HTTP_200_OK
        )


class trainingMaterialCount(APIView):
    Permission_classes = (IsAuthenticated,)

    def post(self, request):
        amount = AIModel.objects.get(ai_id=request.data['ai_id'])
        amount.ai_training_material_count = request.data['ai_traning_material_count']
        amount.save()
        return Response(
            data={"code": 200, "message": "AImodel updated."},
            status=HTTP_200_OK
        )
class unlockedModel(APIView):
    Permission_classes=(IsAdminUser,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        AI_instance.ai_frozen = 0
        AI_instance.save()
        res = {}
        res['code'] = 200
        res['message'] = 'The AI model is successfully unfrozen' 
        return Response(res)


class updatePublished(APIView):
    Permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        tmp = request.data['publish']
        list = [0,1]
        if AI_instance.ai_frozen == 0:
            res['code'] = 200
            res['message'] = 'The AI model publish data cannot changed'
        else:
            if  tmp in list:
                AI_instance.ai_published = tmp
                AI_instance.save()
                res['code'] = 200
                res['message'] = 'The AI model publish data update'
            elif tmp == 2:
                AI_instance.ai_frozen = 0
                AI_instance.save()
                res['code'] = 200
                res['message'] = 'The AI model publish data update'
            else:
                res['code'] = 400
                res['message'] = 'Invalid request'
        return Response(res)

# count how many training materials are passed in to train model
class trainingMaterialCount(APIView):
    Permission_classes = (IsAuthenticated,)

    def post(self, request):
        amount = AIModel.objects.get(ai_id=request.data['ai_id'])
        amount.ai_training_material_count = request.data['ai_traning_material_count']
        amount.save()
        return Response(
            data={"code": 200, "message": "AImodel updated."},
            status=HTTP_200_OK
        )

class personalAImodel(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        response = {}
        user_id = request.data['user_id']
        author = UserProfile.objects.get(id=user_id)
        AIlist = author.aimodel_set.filter(ai_frozen=0)
        res = {}
        res['code'] = 200
        res['message'] = 'get success'
        response['list'] = json.loads(serializers.serialize("json", AIlist))
        res['data'] = response
        return JsonResponse(res)


class updateAIM(APIView):
    permission_classes = (IsAuthenticated,)

    def post(sef,request):
        id = request.data['ai_id']
        AIM = AIModel.objects.get(ai_id = id)
        AIM.ai_name = request.data['ai_name']
        AIM.ai_credit = request.data['model_price']
        AIM.ai_description = request.data['model_intro']
        AIM.ai_type = request.data['model_type']
        AIM.ai_published = request.data['is_published']
        AIM.save()
        return Response(
            data={"code": 200, "message": "bingo!"},
            status=HTTP_200_OK
        )

#增加AI模型访问次数 increase AIM usage
class increaseAIMusage(APIView):
    Permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_instance = AIModel.objects.get(ai_id=request.data['ai_id'])
        AI_instance.ai_AIM_usage += 1
        AI_instance.save()
        return Response(
            data={"code": 200, "message": "AImodel updated."},
            status=HTTP_200_OK
        )

#获取AI模型访问次数 get AIM usage
class getAIMuage(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        AI_model = AIModel.objects.get(ai_id=request.data['ai_id'])
        res = {}
        ai_AIM_usage = AI_model.ai_AIM_usage
        res['code'] = 200
        res['message'] = 'get success'
        res['AIM_usage'] = ai_AIM_usage
        return JsonResponse(res)
