import xadmin

from .models import VerifyCode


class UserProfileAdmin:
    fields = ('name', 'birthdate', 'mobile', 'gender')
    list_display = ('name', 'mobile', 'email', 'gender', 'birthdate')


class VerifyCodeAdmin:
    fields = ('__all__',)
    list_display = ('id', 'status', 'code', 'mobile')


xadmin.site.register(VerifyCode, VerifyCodeAdmin)
