from django.urls import path, re_path
from django.views.generic import TemplateView

app_name = 'face_check'

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'),
         name='index'),
    re_path(
        '^accounts/profile/$',
        TemplateView.as_view(template_name='index.html'),
        name='accounts-profile'
    )
]
