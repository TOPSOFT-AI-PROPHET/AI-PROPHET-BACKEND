from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core import serializers
from .models import Transaction,Cdklist
import json
import uuid

# 生成充值订单
class createCharge(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass # TODO


# 验证充值
class verifyCharge(APIView):
    def post(self, request):
        pass # TODO

# 充钱
class charge(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # each charge is new object and will be stored in database, we need to store user_id, method(充值方式)，order
        Transaction.objects.create(user_id = request.user,status = 1,method = 'charge',order = request.data['order'],credit =  request.data['amount'])
        request.user.credit = request.user.credit + request.data['amount']
        request.user.save()
        return Response(
            data={"code": 200, "message": "Success!","operation":"+" +  str(request.data['amount'])},
            status=HTTP_200_OK
        )

# 扣钱
class deduct(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        Transaction.objects.create(user_id = request.user,status = 1,method = 'deduction',order = request.data['order'],credit =  request.data['amount'])
        request.user.credit = request.user.credit - request.data['amount']
        request.user.save()
        return Response(
            data={"code": 200, "message": "Success!","operation":"-" +  str(request.data['amount'])},
            status=HTTP_200_OK
        )

# 激活码充值
class codecharge(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        # verifie whether the cdk is used
        result = Cdklist.objects.filter(cdk = request.data['code'])
        if (len(result) == 0 or result[0].is_used == 1):
            return Response(
            data={"code": 100, "message": "Failed"},
            status=HTTP_200_OK
            )

        # same as "charge" shown above
        Transaction.objects.create(user_id = request.user,status = 1,method = 'charge',order = "topup",credit =  result[0].amount)
        result[0].is_used = 1
        request.user.credit = request.user.credit + result[0].amount
        result[0].save()
        request.user.save()
        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

class generatecdk(APIView):
    permission_classes = (IsAdminUser,)
    def post(self, request):

        # generate cdk and insert into cdklist
        Cdklist.objects.create(cdk = str(uuid.uuid4()), amount = request.data['amount'])

        return Response(
            data={"code": 200, "message": "Success!"},
            status=HTTP_200_OK
        )

class PersonalTrans(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        id = request.data['user_id']
        response = {}
        Translist = Transaction.objects.filter(user_id = id)
        response['list'] = json.loads(serializers.serialize("json",Translist))

        res = {}
        res['status'] = 200
        res['message'] = 'get success'
        res['data'] = response
        return JsonResponse(res)
