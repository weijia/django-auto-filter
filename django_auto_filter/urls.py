from django.conf.urls import patterns, url
from django_auto_filter.views_django_auto_filter_new import DjangoAutoFilterNew

urlpatterns = patterns('',
                       url(r'^$', DjangoAutoFilterNew.as_view()),
                       )
