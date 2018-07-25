from django.db import models

from users.models import BaseModel, UserProfile
from goods.models import Goods


class UserFav(BaseModel):
    """用户收藏"""
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="用户")
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name="商品")

    class Meta:
        verbose_name = verbose_name_plural = '用户收藏'
        unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


class UserLeavingMessage(BaseModel):
    """用户留言"""
    MESSAGE_CHOICES = (
        (1, "留言"),
        (2, "投诉"),
        (3, "询问"),
        (4, "售后"),
        (5, "求购")
    )
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="用户")
    message_type = models.IntegerField(choices=MESSAGE_CHOICES, verbose_name="留言类型")
    subject = models.CharField(max_length=100, verbose_name="主题")
    message = models.TextField(verbose_name="留言内容")
    file = models.FileField(upload_to="message/images/", verbose_name="上传的文件")

    class Meta:
        verbose_name = verbose_name_plural = '用户留言'

    def __str__(self):
        return self.subject


class UserAddress(BaseModel):
    """用户收货地址"""
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, verbose_name="用户")
    province = models.CharField(max_length=8, verbose_name="省份")
    city = models.CharField(max_length=8, verbose_name="城市")
    district = models.CharField(max_length=16, verbose_name="区域")
    address = models.CharField(max_length=64, verbose_name="详细地址")
    signer_name = models.CharField(max_length=32, verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="电话")

    class Meta:
        verbose_name = verbose_name_plural = '用户收货地址'

    def __str__(self):
        return self.user
