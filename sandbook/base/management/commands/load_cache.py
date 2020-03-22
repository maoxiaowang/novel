from django.core.cache import cache
from django.core.management import BaseCommand

from base.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        # load category novel counts

        categories = Category.objects.prefetch_related('subcategory_set__novel_set')
        for c in categories:
            c_count = 0
            for sc in c.subcategory_set.all():
                sc_count = sc.novel_set.count()
                cache.set(sc.novel_count_key, sc_count)
                c_count += sc_count
            cache.set(c.novel_count_key, c_count)
