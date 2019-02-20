import xadmin

from .adminforms import GoodsAdminForm
from .models import Goods, GoodsCategory, GoodsCategoryBrand, GoodsImage, Banner, HotSearchWords, IndexAd


class GoodsAdmin:
    form = GoodsAdminForm
    list_display = ('id', 'name', 'goods_sn', 'category', 'click_num', 'sold_num', 'shop_price', 'is_new')
    list_filter = ('category', 'shop_price', 'is_new')
    list_editable = ('is_new',)
    search_fields = ('name', 'goods_sn')
    autocomplete_fields = ('category',)
    save_on_top = True
    style_fields = {"goods_desc": "editor"}

    class GoodsImageInline:
        model = GoodsImage
        exclude = ('created_time',)
        extra = 1
        style = 'tab'

    inlines = (GoodsImageInline,)


class GoodsCategoryAdmin:
    list_display = ('name', 'code', 'category_type', 'is_tab')
    list_filter = ('category_type', 'is_tab')
    search_fields = ('name', 'code')


class GoodsCategoryBrandAdmin:
    list_display = ('name', 'desc', 'created_time')

    def get_context(self):
        context = super(GoodsCategoryBrandAdmin, self).get_context()
        if 'form' in context:
            context['form'].fields['category'].queryset = GoodsCategory.objects.filter(category_type=1)
        return context


class BannerAdmin:
    pass


class HotSearchWordsAdmin:
    list_display = ('keywords', 'index')


class IndexAdAdmin:
    list_display = ('goods', 'category')


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(HotSearchWords, HotSearchWordsAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)
