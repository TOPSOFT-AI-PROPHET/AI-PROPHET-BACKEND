from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from .models import UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.parsers import MultiPartParser
import sys
import logging
import uuid

from common.utils.cos import put_object

# 更新用户信息
class updateUserProfile(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        
        request.user.nickname = request.data["nickname"]
        request.user.contact_number = request.data["contact_number"]
        request.user.email = request.data["email"]
        request.user.user_sing = request.data["user_sing"]
        request.user.save()
        return Response(
            data={"code": 200, "message": "Userinfo updated."},
            status=HTTP_200_OK
        )

# 修改用户头像 need to build connection to cos service and use uuid to encrpt it
class updateUserProfileImage(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        file_obj = request.data["avatar"]
        uuid_namespace = uuid.uuid3(uuid.NAMESPACE_OID, str(UserProfile.objects.get(id=request.user.id).id))
        uuid_str = str(uuid.uuid3(uuid_namespace, "avatar")) + ".jpg"

        response = put_object(uuid_str, file_obj.read())

        user = UserProfile.objects.get(id=request.user.id)
        user.profile_image_uuid = uuid_str
        user.save()

        return Response(
            data={"code": 200, "message": "Bingo!", "ETag": response["ETag"], "uuid": uuid_str}, status=HTTP_200_OK
        )


# 获取用户信息
class getUserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        return Response(
            data={"code": 200, "message": "Bingo!", "data": {
                "username": request.user.username,
                "email": request.user.email,
                "nickname": request.user.nickname,
                "credit": request.user.credit,
                "contact_number": request.user.contact_number,
                "profile_image_uuid": request.user.profile_image_uuid,
                "user_sing": request.user.user_sing,
                "user_level": request.user.user_level
            }},
            status=HTTP_200_OK
        )

# 注册用户
class register(APIView):
    def post(self, request):
        if '@' in request.data["username"]:
            return Response(
                data={"code": 403, "message": "Username cannot contain at symbol."},
                status=HTTP_403_FORBIDDEN
            )
        if '@' not in request.data["email"]:
            return Response(
                data={"code": 403, "message": "Email must contain at symbol."},
                status=HTTP_403_FORBIDDEN
            )
        if UserProfile.objects.filter(Q(username=request.data["username"])|Q(email=request.data["email"])):
            return Response(
                data={"code": 403, "message": "Multiple registration."},
                status=HTTP_403_FORBIDDEN
            )
        UserProfile.objects.create(
            username = request.data["username"],
            email = request.data["email"],
            password = make_password(request.data["password"]),
            is_active = True,
            credit = 5
        )
        return Response(
            data={"code": 200, "message": "Registed!"},
            status=HTTP_200_OK
        )

# 找回密码
class forgot(APIView):
    def post(self, request):
        pass # TODO

# 修改密码 use pbkdf2_sha256 to verifie input old password
class changePasswd(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user_old_password = UserProfile.objects.get(id=request.user.id).password
        if not check_password(request.data["old_password"],user_old_password):
            raise ValidationError(
                ('Your old password was entered incorrectly. Please enter it again.')
           )
        elif check_password(request.data["old_password"],user_old_password): 
            request.user.password = make_password(request.data["new_password"], None, 'pbkdf2_sha256')
            request.user.save()
            return Response(
                data={"code": 200, "message": "User password is changed"},
                status=HTTP_200_OK
            )


class returnUsrID(APIView):
    permission_classes = (IsAuthenticated,)

    def post(sef, request):

            return Response(
                data={"code": 200, "message": "Bingo!", "data": {
                    "user_id": request.user.id,
                }},
                status=HTTP_200_OK
            )
