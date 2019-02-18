import random
import time

from rest_framework import serializers

from goods.serializer import GoodsSerializer
from .models import ShoppingCart, Goods, OrderInfo, OrderGoods


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={'min_value': '商品数量不能小于一', "required": '请选择商品数量'})
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            cart_obj = existed[0]
            cart_obj.nums += nums
            cart_obj.save()
        else:
            cart_obj = ShoppingCart.objects.create(**validated_data)

        return cart_obj

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False, read_only=True)

    class Meta:
        model = ShoppingCart
        fields = ('goods', 'nums')


class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderInfoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pay_status = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generate_goods_sn(self):
        return '{ts}{userid}{randstr}'.format(ts=time.strftime('%Y%m%d%H%M%S'),
                                              userid=self.context['request'].user.id,
                                              randstr=random.Random().randint(10, 99))

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_goods_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'
