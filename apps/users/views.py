from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework import status
from rest_framework.response import Response

from utils.yunpian import YunPian
from .models import UserProfile, VerifyCode
from .serializer import SmsSerializer


class CustomBackend(ModelBackend):
    """自定义用户认证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """发送验证码"""
    serializer_class = SmsSerializer

    def send_sms(self, mobile):
        yunpian = YunPian()
        sms_status = yunpian.send(mobile=mobile)
        if sms_status.get('status') != 0:
            return Response({
                'mobile': sms_status.get('mobile'),
                'status': status.HTTP_400_BAD_REQUEST
            })
        VerifyCode.objects.create(code=sms_status.get('sms_code'), mobile=mobile)
        return Response({
            'mobile': sms_status.get('mobile'),
            'status': status.HTTP_201_CREATED,
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data.get('mobile')
        return self.send_sms(mobile=mobile)
