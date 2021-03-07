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
