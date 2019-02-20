from datetime import datetime

from django.conf import settings
from django.shortcuts import redirect
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, \
    OrderDetailSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车
    list:
        购物车详情
    create:
        加入购物车
    """
    serializer_class = ShoppingCartSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'goods_id'

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.goods_num -= instance.nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()


class OrderInfoViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = OrderInfoSerializer
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer  # 订单详情
        return OrderInfoSerializer  # 提交订单

    def perform_create(self, serializer):
        order = serializer.save()
        shopcarts = ShoppingCart.objects.filter(user=self.request.user)
        for shopcart in shopcarts:
            order_goods = OrderGoods()
            order_goods.goods = shopcart.goods
            order_goods.goods_num = shopcart.nums
            order_goods.order = order
            order_goods.save()

            shopcart.delete()
        return order


class AlipayView(APIView):

    def get(self, request):
        """
        处理支付宝的return_url返回
        """
        processed_dict = {}
        # 1. 获取GET中参数
        for key, value in request.GET.items():
            processed_dict[key] = value
        # 2. 取出sign
        sign = processed_dict.pop("sign", None)

        # 3. 生成ALipay对象
        alipay = AliPay(
            appid=settings.APPID,
            app_notify_url=settings.APP_NOTIRY_URL,
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,  # 默认False,
            return_url=settings.RETURN_URL
        )
        verify_re = alipay.verify(processed_dict, sign)
        # 这里可以不做操作。因为不管发不发return url。notify url都会修改订单状态。
        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("/index/#/app/home/member/order")
            return response

        else:
            response = redirect("index")
            return response

    def post(self, request):
        """
        处理支付宝的notify_url
        """
        # 存放post里面所有的数据
        processed_dict = {}
        # 取出post里面的数据
        for key, value in request.POST.items():
            processed_dict[key] = value
        # 把signpop掉，文档有说明
        sign = processed_dict.pop("sign", None)

        # 生成ALipay对象
        alipay = AliPay(
            appid=settings.APPID,
            app_notify_url=settings.APP_NOTIRY_URL,
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,  # 默认False,
            return_url=settings.RETURN_URL
        )
        # 进行验证
        verify_re = alipay.verify(processed_dict, sign)

        # 如果验签成功
        if verify_re is True:
            # 商户网站唯一订单号
            order_sn = processed_dict.get('out_trade_no', None)
            # 支付宝系统交易流水号
            trade_no = processed_dict.get('trade_no', None)
            # 交易状态
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')

            # 查询数据库中订单记录
            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                # 订单商品项
                order_goods = existed_order.goods.all()
                # 商品销量增加订单中数值
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                # 更新订单状态
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()
            # 需要返回一个'success'给支付宝，如果不返回，支付宝会一直发送订单支付成功的消息
            return Response("success")
