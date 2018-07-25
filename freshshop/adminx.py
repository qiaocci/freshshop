import xadmin
from xadmin.views import CommAdminView, BaseAdminView


class BaseSetting(BaseAdminView):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(CommAdminView):
    site_title = '生鲜管理后台'
    site_footer = 'powered by jasonqiao36'


xadmin.site.register(BaseAdminView, BaseSetting)
xadmin.site.register(CommAdminView, GlobalSettings)
