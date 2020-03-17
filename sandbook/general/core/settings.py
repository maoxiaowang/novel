import os
from configparser import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

config_parser = ConfigParser()
config_parser.read('settings.ini')
# default = parser.defaults()

__all__ = [
    'sys_settings',
    'config_parser'
]


class ToDict:

    def to_dict(self):
        result = dict()
        for key, value in self.__class__.__dict__.items():
            if not key.startswith('__') and not callable(getattr(self, key)):
                result[key] = value
        return result


class BaseSettings:

    class MariaDB:
        host = config_parser.get('mariadb', 'host')
        port = config_parser.getint('mariadb', 'port')
        user = config_parser.get('mariadb', 'user')
        password = config_parser.get('mariadb', 'password')
        name = config_parser.get('mariadb', 'name')

    class Memcached:
        hosts = config_parser.get('memcached', 'hosts')

    class RabbitMQ(ToDict):
        host = config_parser.get('rabbitmq', 'host')
        port = config_parser.getint('rabbitmq', 'port')
        user = config_parser.get('rabbitmq', 'user')
        password = config_parser.get('rabbitmq', 'password')
        vhost = config_parser.get('rabbitmq', 'celery_vhost')

    class Email:
        host = config_parser.get('email', 'host')
        port = config_parser.get('email', 'port')
        user = config_parser.get('email', 'user')
        password = config_parser.get('email', 'password')


class Settings(BaseSettings):
    class Celery:
        broker_url = ('amqp://%(user)s:%(password)s@%(host)s:%(port)d/%(vhost)s' %
                      BaseSettings.RabbitMQ().to_dict())
        # result_backend = ('redis://:%(password)s@%(host)s:%(port)d/%(celery_db)d' %
        #                   BaseSettings.Redis().to_dict())


sys_settings = Settings()
