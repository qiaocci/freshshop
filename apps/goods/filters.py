from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Goods


class GoodsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    pricemin = filters.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filters.NumberFilter(field_name="shop_price", lookup_expr='lte')
    top_category = filters.NumberFilter(method='top_category_filter', field_name='category')

    def top_category_filter(self, queryset, name, value):
        """获取一级分类下的所有商品"""
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category=value))

    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemax', 'is_hot', 'is_new']
