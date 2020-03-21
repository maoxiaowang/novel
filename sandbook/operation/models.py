from django.db import models

# Create your models here.


class OperationLog(models.Model):
    novel = models.ForeignKey('base.Novel', on_delete=models.CASCADE)
    manager = models.ForeignKey('base.User', on_delete=models.CASCADE)
    action = models.CharField('动作', max_length=255)

    class Meta:
        db_table = 'base_manager_operation'
        default_permissions = ()
