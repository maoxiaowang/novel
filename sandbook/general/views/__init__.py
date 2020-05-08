from django.views.generic import DetailView, ListView, DeleteView

from general.views.mixin import JSONResponseMixin


class JSONDetailView(JSONResponseMixin, DetailView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.json_response(data=self.object)


class JSONDeleteView(JSONResponseMixin, DeleteView):

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.json_response()


# class JSONListView(JSONResponseMixin, ListView):
#
#     def get(self, request, *args, **kwargs):
