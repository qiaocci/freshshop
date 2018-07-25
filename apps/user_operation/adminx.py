import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress


class UserFavAdmin:
    list_display = ('user', 'goods')


class UserLeavingMessageAdmin:
    list_display = ('user', 'message_type', 'subject')


class UserAddressAdmin:
    list_display = ('user', 'province', 'city', 'signer_name', 'signer_mobile')


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
