from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from django_auto_filter.views_django_auto_filter import DjangoAutoFilter
from djangoautoconf.model_utils.model_attr_utils import model_enumerator
from ufs_tools.string_tools import class_name_to_low_case


def add_filter_to_url_for(urlpatterns, models):
    for model in model_enumerator(models):
        urlpatterns += patterns('', url(r'^models/%s/' % class_name_to_low_case(model.__name__),
                                        DjangoAutoFilter.as_view(model=model)))


def get_filter_urls(models, template_name=None):
    url_list = []
    for model in model_enumerator(models):
        param_dict = {"model": model}
        if template_name is not None:
            param_dict["template_name"] = template_name
        url_list.append(url(r'^model/%s/' % class_name_to_low_case(model.__name__),
                            login_required(DjangoAutoFilter.as_view(**param_dict))))

    p = patterns('', *url_list)
    return p
