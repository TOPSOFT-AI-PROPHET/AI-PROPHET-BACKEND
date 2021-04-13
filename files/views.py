from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.core.files.base import ContentFile
from django.http import FileResponse
from users.models import UserProfile
from .models import File
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
import uuid
# Create your views here.

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
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        file_obj = request.data['file']
        
        secret_id = 'AKIDZx60e1HAamulLgNW1MUR7WdT6UkktKp4'      # 替换为用户的 secretId
        secret_key = '7xW4KOCiyyoN4WhbDySjjSu42kiPq1vx'      # 替换为用户的 secretKey
        region = 'ap-chengdu'     # 替换为用户的 Region
        token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        # 2. 获取客户端对象
        client = CosS3Client(config)
        uuid_namespace = uuid.uuid3(uuid.NAMESPACE_OID,str(UserProfile.objects.get(id = request.user.id).id))
        uuid_str = str(uuid.uuid3(uuid_namespace, "avatar"))
        response = client.put_object(
        Bucket='prophetsrc-1305001068',
        Body=file_obj.read(),
        Key= uuid_str,
        StorageClass='STANDARD',
        EnableMD5=False)
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