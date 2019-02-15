from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler

from utils.yunpian import YunPian
from .models import UserProfile, VerifyCode
from .serializer import SmsSerializer, UserRegSerializer, UserDetailSerializer


class CustomBackend(ModelBackend):
    """自定义用户认证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """发送验证码"""
    serializer_class = SmsSerializer

    def send_sms(self, mobile):
        yunpian = YunPian()
        return yunpian.send(mobile=mobile)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')
        sms_status = self.send_sms(mobile=mobile)

        if sms_status.get('status') != 0:
            return Response({
                'mobile': sms_status.get('mobile'),
                'status': status.HTTP_400_BAD_REQUEST
            })
        VerifyCode.objects.create(code=sms_status.get('sms_code'), mobile=mobile)
        headers = self.get_success_headers(serializer.data)
        return Response({'mobile': sms_status.get('mobile'), 'status': status.HTTP_201_CREATED, 'headers': headers})


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserRegSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action == 'retrieve':
            """个人中心获取用户详情时，必须是登录状态"""
            return [IsAuthenticated(), ]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            """个人中心获取用户详情时，使用的serializer"""
            return UserDetailSerializer
        elif self.action == 'create':
            return self.serializer_class
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    # def get_object(self):
    #     return self.request.user
