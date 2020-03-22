from django.apps import AppConfig


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        # signals
        import base.signals.account
        base.signals.account.init()
