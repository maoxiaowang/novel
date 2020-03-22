from django.core.management import BaseCommand

from base.constants.account import BUILTIN_GROUPS, BUILTIN_USERS
from base.constants.novel import BUILTIN_CATEGORIES, BUILTIN_SUBCATEGORIES
from base.models import Group, User, Category, SubCategory


class Command(BaseCommand):

    def handle(self, *args, **options):
        # 创建默认组
        exist_groups = Group.objects.values_list('id', flat=True)
        groups = Group.objects.bulk_create(
            [Group(**item) for item in BUILTIN_GROUPS if item['id'] not in exist_groups]
        )
        if groups:
            self.stdout.write(
                self.style.SUCCESS('Successfully created %d groups.' % len(groups))
            )

        # 创建默认用户
        exist_users = User.objects.values_list('id', flat=True)
        users = list()
        user_groups = dict()
        for user in BUILTIN_USERS:
            # 移除并记录groups
            if user['id'] not in exist_users:
                groups = user.pop('groups') if 'groups' in user else []
                user_groups.update({user['id']: groups})
                created = User.objects.create_user(**user)
                users.append(created)
        if users:
            self.stdout.write(
                self.style.SUCCESS('Successfully created %d users.' % len(users))
            )
            for user in users:
                # 添加组
                groups = user_groups[user.id]
                if groups:
                    user.groups.add(*groups)
                    self.stdout.write(
                        self.style.SUCCESS('Successfully add user %s to groups %s.' %
                                           (user.username, ','.join(map(lambda g: str(g), groups))))
                    )

        # 创建默认一级分类
        exist_categories = Category.objects.values_list('id', flat=True)
        categories = Category.objects.bulk_create(
            [Category(**item) for item in BUILTIN_CATEGORIES if item['id'] not in exist_categories]
        )
        if categories:
            self.stdout.write(
                self.style.SUCCESS('Successfully created %d categories.' % len(categories))
            )

        # 创建默认二级分类
        exist_sub_categories = SubCategory.objects.values_list('id', flat=True)
        sub_categories = SubCategory.objects.bulk_create(
            [SubCategory(**item) for item in BUILTIN_SUBCATEGORIES if item['id'] not in exist_sub_categories]
        )
        if sub_categories:
            self.stdout.write(
                self.style.SUCCESS('Successfully created %d sub categories.' % len(sub_categories))
            )
