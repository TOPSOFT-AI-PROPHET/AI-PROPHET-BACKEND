from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser
from django.core.files.base import ContentFile
from django.http import FileResponse
from .models import File
# Create your views here.

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

class getFile(APIView):
    def get(self, request):
        uuid = request.GET.get('uuid')
        if uuid :
            file_obj = File.objects.get(file_uuid=uuid)
            if file_obj :
                response = FileResponse(ContentFile(file_obj.file_bin), filename=file_obj.file_name)
                response['Content-Type'] = 'application/octet-stream'
                return response
        return Response(
            data={"code": 403, "message": "file error!"},
            status=HTTP_403_FORBIDDEN
        )