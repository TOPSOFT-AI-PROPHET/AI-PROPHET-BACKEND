from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.core.files.base import ContentFile
from django.http import FileResponse
from users.models import UserProfile
from .models import File
import sys
import logging
import uuid
import time

from common.utils.cos import put_object

# 上传文件
class uploadFile(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        file_obj = request.data['file']
        if file_obj :
            theFile = File.objects.create(
                file_name=file_obj.name,
                file_bin=file_obj.read()
            )
            return Response(
                data={"code": 200, "message": "Bingo!", "uuid": theFile.file_uuid},
                status=HTTP_200_OK
            )
        return Response(
            data={"code": 403, "message": "file error!"},
            status=HTTP_403_FORBIDDEN
        )

# 上传文件_cos
class uploadFile_cos(APIView):
    parser_classes = [MultiPartParser] # for uploading different data in different data type
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        file_obj = request.FILES['upload_file']
        
        uuid_namespace = uuid.uuid4()
        uuid_str = str(uuid_namespace)+str(time.time())
        response = put_object(file_obj.read(), uuid_str)
       
        user = UserProfile.objects.get(id = request.user.id)
        user.profile_image_uuid = uuid_str
        user.save()
        return Response(
            data={"code": 200, "message": "Bingo!","ETag":response['ETag'],"uuid":uuid_str},
            status=HTTP_200_OK
        )

# 下载文件
class getFile(APIView):
    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid :
            try:
                file_obj = File.objects.get(file_uuid=uuid)
                if file_obj :
                    # please refer to cos offical documentation to understand 
                    response = FileResponse(ContentFile(file_obj.file_bin), filename=file_obj.file_name)
                    response['Content-Type'] = 'application/octet-stream'
                    return response
            except:
                pass
        return Response(
            data={"code": 403, "message": "file error!"},
            status=HTTP_403_FORBIDDEN
        )

# 删除文件
class delFile(APIView):
    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid :
            try:
                # please refer to cos offical documentation to understand 
                File.objects.get(file_uuid=uuid).delete()
                return Response(
                    data={"code": 200, "message": "Bingo!"},
                    status=HTTP_200_OK
                )
            except:
                pass
        return Response(
            data={"code": 403, "message": "file error!"},
            status=HTTP_403_FORBIDDEN
        )