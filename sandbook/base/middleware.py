import traceback

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from general.core.logging import get_logger
from general.views import JSONResponseMixin

logger = get_logger('middleware')


class ExceptionProcessingMiddleware(MiddlewareMixin):

    # def __init__(self, get_response):
    #     # self.get_response = get_response
    #     self.mongo_log_db = MongoDB().col_opt_log()
    #     super().__init__(get_response)
    #     # One-time configuration and initialization.
    #     # Initialize first starting of the system

    # def __call__(self, request):
    #     # Code to be executed for each request before
    #     # the view (and later middleware) are called.
    #     super().__call__(request)
    #     response = self.get_response(request)
    #
    #     # Code to be executed for each request/response after
    #     # the view is called.
    #
    #     return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """
        call before view executing
        """
        if JSONResponseMixin in view_func.__class__.__bases__:
            request.response_type = 'json'
        else:
            request.response_type = 'html'

    def process_exception(self, request, exception):
        """
        Call when raise an exception
        """
        if request.response_type == 'json':
            code = 500
            level = 'error'
            data = None
            if isinstance(exception, PermissionDenied):
                messages = '权限不足'
                level = 'warning'
                code = 403
            elif isinstance(exception, ObjectDoesNotExist):
                messages = list()
                for item in exception.args:
                    messages.append('对象不存在 %s' % item)
                level = 'error'
                code = 404
            elif isinstance(exception, ValidationError):
                code = 402
                messages = exception.message
            else:
                messages = str(exception)
                logger.error(messages)
                logger.error(traceback.format_exc())
            return JSONResponseMixin.json_response(
                result=False, messages=messages, code=code, level=level, data=data
            )

