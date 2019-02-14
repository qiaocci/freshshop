"""freshshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
# from rest_framework_jwt.views import obtain_jwt_token
from xadmin.plugins import xversion

from goods.views import GoodsListViewSet, GoodsCategoryListViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddressViewSet
from trade.views import ShoppingCartViewSet
from users.views import SmsCodeViewset, UserViewset
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

router = DefaultRouter()
router.register('goods', GoodsListViewSet, base_name='goods')
router.register('categories', GoodsCategoryListViewSet, base_name='category')
router.register('code', SmsCodeViewset, base_name='code')
router.register('users', UserViewset, base_name='users')
router.register('userfavs', UserFavViewSet, base_name='userfavs')
router.register('messages', UserLeavingMessageViewSet, base_name='messages')
router.register('address', UserAddressViewSet, base_name='address')
router.register('shopcarts', ShoppingCartViewSet, base_name='shopcarts')

xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
                  re_path('media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('', include(router.urls)),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('docs/', include_docs_urls(title='生鲜超市', public=False)),
                  # path('login/', obtain_jwt_token),

                  path('admin/', xadmin.site.urls),

                  path('sadmin/', admin.site.urls),

                  # jwt登录
                  path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
