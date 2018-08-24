from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .filters import GoodsFilter
from .models import Goods, GoodsCategory
from .serializer import GoodsSerializer, GoodsCategorySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 40


class GoodsListViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """商品列表"""

    queryset = Goods.objects.all().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = GoodsFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'goods_brief')
    ordering_fields = ('sold_num', 'shop_price')


class GoodsCategoryListViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """商品分类列表"""
    queryset = GoodsCategory.objects.all().filter(category_type=1)
    serializer_class = GoodsCategorySerializer
    # authentication_classes = (TokenAuthentication,)
