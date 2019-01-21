from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage


class GoodsCategorySerializers3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializers2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializers3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsCategorySerializer(serializers.ModelSerializer):
    """商品类别"""
    sub_cat = GoodsCategorySerializers2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = '__all__'

    def create(self, validated_data):
        return Goods.objects.create(**validated_data)
