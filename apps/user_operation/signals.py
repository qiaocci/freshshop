from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UserFav


@receiver(post_save, sender=UserFav)
def userfav_post_save_handler(sender, instance, created, raw, using, **kwargs):
    import pdb;
    pdb.set_trace()
    if created:
        goods = instance.goods
        goods.fav_num += 1
        goods.save()


@receiver(post_delete, sender=UserFav)
def userfav_post_delete_handler(sender, instance, **kwargs):
    goods = instance.goods
    goods.fav_num -= 1
    goods.save()
