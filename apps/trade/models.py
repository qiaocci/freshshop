from django.db import models

from users.models import UserProfile, BaseModel
from goods.models import Goods


class ShoppingCart(BaseModel):
    """购物车"""
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='商品')
    nums = models.IntegerField(verbose_name='商品数量')

    class Meta:
        verbose_name = verbose_name_plural = '购物车'
        unique_together = ('goods', 'user')

    def __str__(self):
        return f'{self.goods.name}:{self.nums}'


class OrderInfo(BaseModel):
    """订单"""
    PAY_STATUS = [
        ('SUCCESS', '成功'),
        ('CANCEL', '取消'),
        ('PAYING', '待支付'),
    ]
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=13, null=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=13, null=True, unique=True, verbose_name='外部交易号')
    pay_status = models.CharField(max_length=32, default='paying', choices=PAY_STATUS, verbose_name='支付状态')
    post_script = models.CharField(max_length=128, verbose_name='订单留言')
    order_mount = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='订单时间')

    # 用户信息
    address = models.CharField(max_length=128, verbose_name="收货地址")
    signer_name = models.CharField(max_length=16, verbose_name="签收人")
    singer_mobile = models.CharField(max_length=11, verbose_name="联系电话")

    class Meta:
        verbose_name = verbose_name_plural = '订单'

    def __str__(self):
        return self.order_sn


class OrderGoods(BaseModel):
    """订单中商品的信息"""
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name="订单信息", related_name="goods")
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name="商品")
    goods_num = models.IntegerField(verbose_name="商品数量")

    class Meta:
        verbose_name = verbose_name_plural = '订单'

    def __str__(self):
        return self.order.order_sn
