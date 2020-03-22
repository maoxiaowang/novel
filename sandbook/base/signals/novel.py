from django.db.models.signals import post_save
from django.dispatch import receiver

from base.models import Novel
from base.models.novel import Volume


@receiver(post_save, sender=Novel)
def on_novel_changed(sender, instance, **kwargs):
    if kwargs.get('created'):
        # 创建默认卷
        Volume.objects.create(novel=instance)
    else:
        ...
