from django.conf import settings

from general.views import JSONResponseMixin


class FormValidationMixin(JSONResponseMixin):
    """
    non_field_replacement must be a field name
    """
    non_field_replacement = None
    json = False

    def dispatch(self, request, *args, **kwargs):
        if 'json' in request.GET:
            self.json = True
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if self.json:
            return
        return super().get_success_url()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.json:
            data = self.object if hasattr(self, 'object') else {}
            return self.json_response(data=data)
        return response

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
