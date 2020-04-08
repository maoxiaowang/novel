import typing

from django.contrib.auth import mixins as auth_mixin
from django.http import JsonResponse
from django.utils.functional import Promise

from general.core.serializer import SJSONEncoder


class JSONResponseMixin:

    @staticmethod
    def json_response(result: bool = True, messages: list = None,
                      level=None, code=200, data=None, default_msg=True,
                      **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        QuerySet data will be transformed into a special format.
        """
        assert isinstance(result, bool)
        if level is None:
            level = 'success' if result else 'error'
        assert level in ('success', 'info', 'warning', 'error')
        if messages is None and default_msg:
            messages = ['操作成功'] if result else ['操作失败']
        if isinstance(messages, (str, Promise)):
            messages = [str(messages)]
        assert isinstance(messages, typing.Iterable)
        messages = [str(m) for m in messages]
        assert isinstance(code, int)
        if not result and code <= 300:
            code = 400
            level = 'error'
        elif result and code >= 300:
            code = 200
            level = 'success'

        empty_data = [] if isinstance(data, list) else {}
        data = {
            'result': result,
            'messages': messages or [],
            'level': level,
            'code': code,
            'data': data or empty_data
        }
        response = JsonResponse(
            data,
            encoder=SJSONEncoder,
            **response_kwargs
        )

        return response


class LoginRequiredMixin(auth_mixin.LoginRequiredMixin):
    raise_exception = True
    permission_denied_message = '需要登录'
