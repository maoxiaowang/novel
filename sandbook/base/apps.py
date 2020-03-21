from django.apps import AppConfig
from django.core.cache import cache


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        # signals
        import base.signals.account
        base.signals.account.init()

        # load category novel counts
        from base.models import Category

        categories = Category.objects.prefetch_related('subcategory_set__novel_set')
        for c in categories:
            c_count = 0
            for sc in c.subcategory_set.all():
                sc_count = sc.novel_set.count()
                cache.set(sc.novel_count_key, sc_count)
                c_count += sc_count
            cache.set(c.novel_count_key, c_count)
