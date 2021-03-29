from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from .models import Transaction
import json

# 生成充值订单
class createCharge(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        pass # TODO

# 充值历史
class listCharge(APIView):
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
        Transaction.objects.create(user_id = request.user,status = 1,method = request.data['method'],order = request.data['order'],credit =  request.data['amount'])
        request.user.credit = request.user.credit + request.data['amount']
        request.user.save()
        return Response(
            data={"code": 200, "message": "Success!","opreation":"+" +  str(request.data['amount'])},
            status=HTTP_200_OK
        )

# 扣钱
class deduct(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        Transaction.objects.create(user_id = request.user,status = 1,method = request.data['method'],order = request.data['order'],credit =  request.data['amount'])
        request.user.credit = request.user.credit - request.data['amount']
        request.user.save()
        return Response(
            data={"code": 200, "message": "Success!","opreation":"-" +  str(request.data['amount'])},
            status=HTTP_200_OK
        )
