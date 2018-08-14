import datetime
import re

from rest_framework import serializers

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
