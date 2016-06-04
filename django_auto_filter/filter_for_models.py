from django.conf.urls import patterns, url, include
from djangoautoconf.model_utils.model_attr_utils import model_enumerator
from djangoautoconf.tastypie_utils import create_tastypie_resource
from ufs_tools.string_tools import class_name_to_low_case
from django_auto_filter.views_django_auto_filter import DjangoAutoFilter


def add_filter_to_url_for(urlpatterns, models):
    for model in model_enumerator(models):
        urlpatterns += patterns('', url(r'^models/%s/' % class_name_to_low_case(model.__name__),
                                        DjangoAutoFilter.as_view(model_class=model)))


def get_filter_urls(models, template_name=None):
    url_list = []
    for model in model_enumerator(models):
        param_dict = {"model_class": model}
        if template_name is None:
            param_dict["template_name"] = template_name
        url_list.append(url(r'^model/%s/' % class_name_to_low_case(model.__name__),
                            DjangoAutoFilter.as_view(**param_dict)))

    p = patterns('', *url_list)
    return p
