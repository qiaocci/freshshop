from django.db import models

from users.models import BaseModel


class GoodsCategory(BaseModel):
    """商品分类"""
    CATEGORY_ITEMS = [
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类'),
    ]
    name = models.CharField(max_length=64, help_text='名称', verbose_name='名称')
    code = models.CharField(max_length=32, help_text='编码', verbose_name='分类编码')
    desc = models.TextField(help_text='描述', verbose_name='描述')
    category_type = models.PositiveSmallIntegerField(choices=CATEGORY_ITEMS, verbose_name='级别')
    parent_category = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING,
                                        related_name='sub_cat', verbose_name='父级分类')
    is_tab = models.BooleanField(default=False, verbose_name='是否导航')

    class Meta:
        verbose_name = verbose_name_plural = '商品分类'

    def __str__(self):
        return self.code


class GoodsCategoryBrand(BaseModel):
    """一级分类下的品牌名称"""
    name = models.CharField(max_length=64, verbose_name='名称')
    category = models.ForeignKey(GoodsCategory, on_delete=models.DO_NOTHING, verbose_name='商品分类')
    desc = models.TextField(verbose_name='描述')
    image = models.ImageField(max_length=200, upload_to='brands/', verbose_name='图标')

    class Meta:
        verbose_name = verbose_name_plural = '品牌'

    def __str__(self):
        return self.name


class Goods(BaseModel):
    """商品"""
    name = models.CharField(max_length=128, verbose_name='商品名')
    goods_sn = models.CharField(max_length=64, verbose_name='唯一货号')
    category = models.ForeignKey(GoodsCategory, on_delete=models.DO_NOTHING, verbose_name='分类')
    click_num = models.IntegerField(default=0, verbose_name='点击数')
    sold_num = models.IntegerField(default=0, verbose_name='销售量')
    fav_num = models.IntegerField(default=0, verbose_name='收藏数')
    goods_num = models.IntegerField(default=0, verbose_name='库存数')
    market_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='市场价')
    shop_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='销售价')
    goods_brief = models.TextField(verbose_name='简短描述')
    goods_desc = models.TextField(verbose_name='详细描述')
    ship_free = models.BooleanField(default=False, verbose_name='是否免运费')
    goods_front_image = models.ImageField(upload_to='goods/images/', null=True, blank=True, verbose_name='封面图')
    is_new = models.BooleanField(verbose_name='是否新品')
    is_hot = models.BooleanField(verbose_name='是否热销')

    class Meta:
        verbose_name = verbose_name_plural = '商品'
        ordering = ('id',)

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """商品轮播图"""
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品', related_name='images')
    image = models.ImageField(upload_to='goods/images/', verbose_name='图片')

    class Meta:
        verbose_name = verbose_name_plural = '商品图片'

    def __str__(self):
        return self.goods.name


class Banner(BaseModel):
    """轮播的商品"""
    goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, verbose_name='商品')
    image = models.ImageField(upload_to='banner', verbose_name='轮播图')
    index = models.IntegerField(verbose_name='轮播顺序')

    class Meta:
        verbose_name = verbose_name_plural = '轮播商品'

    def __str__(self):
        return self.goods.name


class HotSearchWords(BaseModel):
    """热搜词"""
    keywords = models.CharField(max_length=16, verbose_name='热搜词')
    index = models.IntegerField(verbose_name='顺序')

    class Meta:
        verbose_name = verbose_name_plural = '热搜'

    def __str__(self):
        return self.keywords
