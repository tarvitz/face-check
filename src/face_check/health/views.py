from django.views.generic import View
from django.http import HttpResponse


class StatusView(View):
    def get(self, request):
        return HttpResponse('ok')


class HealthView(StatusView):
    """
    Health View
    """
