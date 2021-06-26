from django.urls import path
from .views import *

urlpatterns = [
    path('createCharge', createCharge.as_view(), name="createCharge"),
    path('listCharge', listCharge.as_view(), name="listCharge"),
    path('verifyCharge', verifyCharge.as_view(), name="verifyCharge"),
    path('charge', charge.as_view(), name="charge"),
    path('deduct', deduct.as_view(), name="deduct"),
    path('codecharge', codecharge.as_view(), name="codecharge"),
]
