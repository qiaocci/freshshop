from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .filters import GoodsFilter
from .models import Goods, GoodsCategory, Banner, HotSearchWords
from .serializer import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, HotWordsSerializer, \
    IndexCategorySerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 40


class GoodsListViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """商品列表
        list: 商品列表
        retrieve: 商品详情
    """

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = GoodsFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')


class GoodsCategoryListViewSet(mixins.ListModelMixin,
                               mixins.RetrieveModelMixin,
                               viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.all().filter(category_type=1)
    serializer_class = GoodsCategorySerializer


class BannerViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


class HotSearchsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by("-index")
    serializer_class = HotWordsSerializer


class IndexCategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=["生鲜食品", "酒水饮料"])
    serializer_class = IndexCategorySerializer
