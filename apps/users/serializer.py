import datetime
import re
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import VerifyCode, UserProfile


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, value):
        """
        检查手机号是否有效
        """
        pattern = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        if not re.match(pattern, str(value)):
            raise serializers.ValidationError('手机号码格式不正确')
        if UserProfile.objects.filter(mobile=value).count() > 0:
            raise serializers.ValidationError('mobile has been registered')
        one_minute_ago = datetime.datetime.now() - datetime.timedelta(minutes=1)
        if VerifyCode.objects.filter(created_time__gt=one_minute_ago, mobile=value).count():
            raise serializers.ValidationError('send too quickly')
        return value


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=6, min_length=6, write_only=True, label='验证码',
                                 error_messages={'blank': '请输入验证码', 'max_length': '验证码长度错误',
                                                 'min_length': '验证码长度错误'})
    username = serializers.CharField(required=True, allow_blank=False, label='用户名',
                                     validators=[UniqueValidator(queryset=UserProfile.objects.all(), message='用户已存在')])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, label='密码')

    def validate_code(self, code):
        five_minutes_ago = timezone.now() - datetime.timedelta(days=5)
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data.get('username')).order_by('-id')
        if verify_records:
            last_record = verify_records[0]
            if five_minutes_ago > last_record.created_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data['password'])
    #     return super().create(validated_data)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'code', 'mobile')
