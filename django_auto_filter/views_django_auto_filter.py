from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.db import models
from django.db.models import Q
from django.views.generic import TemplateView
from django_tables2_reports.tables import TableReport
from django_tables2_reports.config import RequestConfigReport as RequestConfig
from django_tables2_reports.utils import create_report_http_response

from django_tables2.utils import A  # alias for Accessor

from django_auto_filter.filter_generator import FilterGenerator
from django_auto_filter.table_generator import TableGenerator
from djangoautoconf.model_utils.url_for_models import get_rest_api_url

__author__ = 'weijia'


class DjangoAutoFilter(TemplateView):
    template_name = 'django_auto_filter/filters.html'
    model = User
    # filter_fields = {"username": ["icontains"]}
    # The following is also OK
    # filter_fields = ["username", ]
    edit_namespace = "admin"
    item_per_page = 10
    url_name = None

    def __init__(self, **kwargs):
        super(DjangoAutoFilter, self).__init__(**kwargs)
        self.table_to_report = None

    def get_context_data(self, **kwargs):
        context = super(DjangoAutoFilter, self).get_context_data(**kwargs)

        filter_generator = FilterGenerator(self.model)

        table_generator = TableGenerator(self.model)
        table = table_generator.get_table_from_queryset(filter_generator.get_query_set(self.request.GET))

        self.table_to_report = RequestConfig(self.request, paginate={"per_page": self.item_per_page}).configure(table)
        context.update({"table": table, "filter": (filter_generator.get_filter_instance(self.request.GET)),
                        "admin_base_url": self.get_admin_url(),
                        "model_rest_api_url": (get_rest_api_url(self.model))})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not (self.table_to_report is None):
            return create_report_http_response(self.table_to_report, self.request)
        return self.render_to_response(context)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.model)
        if self.url_name is None:
            url_name = "%s:%s_%s_change" % (self.edit_namespace, content_type.app_label, content_type.model)
        else:
            url_name = "%s:%s" % (self.edit_namespace, self.url_name)
        url = urlresolvers.reverse(url_name, args=("1",))
        url = url.replace("1", "%d")
        return url
