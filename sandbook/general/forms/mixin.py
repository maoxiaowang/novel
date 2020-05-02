from django.conf import settings
from django.http import HttpResponseRedirect

from general.views import JSONResponseMixin


class FormValidationMixin(JSONResponseMixin):
    """
    Only for ModelFormMixin
    non_field_replacement must be a field name
    """
    non_field_replacement = None
    json = False
    ajax = False

    def dispatch(self, request, *args, **kwargs):
        if 'json' in request.GET or 'json' in request.POST:
            self.json = True
            self.ajax = True
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.ajax:
            return
        return super().get_success_url()

    def _template_response(self):
        raise ValueError("Mode 'ajax' can not be set without 'json'.")

    def form_valid(self, form):
        super().form_valid(form)
        if self.json:
            data = self.object if hasattr(self, 'object') else {}
            return self.json_response(data=data)
        else:
            success_url = self.get_success_url()
            if success_url is not None:
                return HttpResponseRedirect(success_url)
        return self._template_response()

    def form_invalid(self, form):
        # Append css class to every field that contains errors.
        if self.json:
            if settings.DEBUG:
                msgs = list()
                for k, el in form.errors.items():
                    for item in el:
                        msgs.append('[%s] %s' % (k, item))
            else:
                msgs = [' '.join(v) for f, v in form.errors.items()]
            return self.json_response(result=False, messages=msgs)
        else:
            for field in form.errors:
                if field == '__all__':
                    if self.non_field_replacement:
                        field = self.non_field_replacement
                    else:
                        continue
                form[field].field.widget.attrs['class'] += ' is-invalid'
            return super().form_invalid(form)
