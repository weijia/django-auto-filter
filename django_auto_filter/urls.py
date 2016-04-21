from django.conf.urls import patterns, url
from django_auto_filter.views_django_auto_filter import DjangoAutoFilter

urlpatterns = patterns('',
                       url(r'^$', DjangoAutoFilter.as_view()),
                       )
