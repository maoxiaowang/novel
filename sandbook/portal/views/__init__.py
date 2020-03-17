from django.views.generic.base import View, TemplateView


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return kwargs
