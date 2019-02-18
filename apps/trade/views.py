from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

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
