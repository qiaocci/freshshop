from rest_framework import serializers

from .models import ShoppingCart, Goods


class ShoppingCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    nums = serializers.IntegerField(required=True, min_value=1, label='数量',
                                    error_messages={'min_value': '商品数量不能小于一', "required": '请选择商品数量'})
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = validated_data['user']
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
