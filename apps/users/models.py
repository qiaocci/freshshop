from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    STATUS_ITEMS = [
        (1, '正常'),
        (0, '删除'),
    ]

    status = models.PositiveIntegerField(choices=STATUS_ITEMS, default=1, db_index=True, verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True


class UserProfile(AbstractUser, BaseModel):
    GENDER_ITEMS = [
        (0, '未知'),
        (1, '男'),
        (2, '女')
    ]

    name = models.CharField(max_length=32, null=True, verbose_name='姓名')
    birthdate = models.DateField(null=True, verbose_name='出生日期')
    mobile = models.CharField(max_length=11, null=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_ITEMS, default=0, verbose_name='性别')
    email = models.EmailField(max_length=64, null=True, verbose_name='邮箱')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = verbose_name_plural = '用户'

    def __str__(self):
        return self.name


class VerifyCode(BaseModel):
    """短信验证码"""
    code = models.CharField(max_length=10, verbose_name='验证码')
    mobile = models.CharField(max_length=11, verbose_name='电话')

    class Meta:
        verbose_name = verbose_name_plural = '短信验证码'

    def __str__(self):
        return self.code
