from ajax_select import make_ajax_form
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import urlresolvers
from django.db.models import Q
from django.views.generic import TemplateView
import django_filters
from django_tables2_reports.tables import TableReport
from django_tables2_reports.config import RequestConfigReport as RequestConfig
from django_tables2_reports.utils import create_report_http_response
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from djangoautoconf.model_utils.model_attr_utils import enum_model_fields
from tagging_app.tagging_app_utils import get_tag_str_from_tag_list

__author__ = 'weijia'


def render_tags(self, value):
    return get_tag_str_from_tag_list(value)


class DjangoAutoFilter(TemplateView):
    template_name = 'django_auto_filter/filters.html'
    model_class = User
    filter_fields = {"username": ["icontains"]}
    # The following is also OK
    # filter_fields = ["username", ]
    edit_namespace = "admin"
    # Used by django-ajax-selects
    ajax_fields = {}
    # ajax_fields = {"relations": "ufs_obj", "parent": "ufs_obj", "descriptions": "description"}
    # additional_col = {"tags":
    #                       tables.Column(
    # # #                       tables.TemplaColumn('''
    # # # <span class="tagged-item editable editable-click"
    # # #    {{ record|gen_tag_attr }}> {{ record.tags }}
    # # # </span>
    # # # ''',
    #                                           attrs={'th': {"data-editable": "true"},
    #             'td': {"objectId": "{{ record.id }}",  "tags": A("record.tags"), "contentType": 83}})}
    additional_col = {
        # The following line make the column editable (work for x editable)
        "tags": tables.Column(attrs={'th': {"data-editable": "true"}}),
        "render_tags": render_tags,
        "row_info": tables.TemplateColumn('<span {{ record|gen_tag_attr }}> </span>',
                                          # Hide this column
                                          attrs={'th': {"class": "hidden-column"},
                                                 "td": {"class": "hidden-column"}},
                                          ),
    }

    def __init__(self, **kwargs):
        super(DjangoAutoFilter, self).__init__(**kwargs)
        # self.model_class = None
        self.choice_fields = {}
        self.text_fields = {}
        self.table_to_report = None
        self.ajax_form = None

    def get_contains_all_keyword_form(self):
        form_class = type(self.model_class.__name__ + "ContainAllKeywordForm", (forms.ModelForm,), {
            "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
            "keywords": forms.CharField(required=False),
        })
        return form_class

    def render_edit(self):
        return '%d' % next(self.counter)

    def get_table_report_class(self):
        content_type = ContentType.objects.get_for_model(self.model_class)
        attr_dict = {
            "Meta": type("Meta", (), {
                "model": self.model_class,
                "sequence": ["id", "tags"],
                # "row_attrs": {
                #     # 'data-id': lambda record: record.pk
                #     "objectId": lambda record: record.pk,
                #     "tags": lambda record: record.tags,
                #     "content-type": lambda record: ContentType.objects.get_for_model(record).pk,
                #     "data-name": "tags",
                # }
            }),
            # "edit": tables.Column(),
            # "render_edit":
            # "edit": tables.LinkColumn("admin:%s_%s_change" %
            #                           (content_type.app_label, content_type.model), args=[A('pk')])

        }
        attr_dict.update(self.additional_col)
        table_class = type(self.model_class.__name__ + "AutoTable", (TableReport,), attr_dict)
        return table_class

    def get_filter_class(self):
        self.set_ajax_form()
        self.set_fields()
        class_attr = {
            "Meta": type("Meta", (),
                         {"model": self.model_class,
                          "form": self.ajax_form,
                          "fields": self.text_fields,
                          }),
        }
        class_attr.update(self.choice_fields)

        filter_class = type(self.model_class.__name__ + "AutoFilter", (django_filters.FilterSet,), class_attr)
        return filter_class

    def set_fields(self):
        for attr in enum_model_fields(self.model_class):
            if attr.name not in self.ajax_fields:
                if hasattr(attr, "choices") and len(attr.choices):
                    self.choice_fields[attr.name] = django_filters.MultipleChoiceFilter(choices=attr.choices)
                else:
                    self.text_fields[attr.name] = ["icontains"]

    def set_ajax_form(self):
        self.ajax_form = make_ajax_form(self.model_class, self.ajax_fields, self.get_contains_all_keyword_form())
        for field in self.ajax_form.declared_fields:
            self.ajax_form.declared_fields[field].required = False

    def get_context_data(self, **kwargs):
        context = super(DjangoAutoFilter, self).get_context_data(**kwargs)
        keyword_form = self.get_contains_all_keyword_form()(self.request.GET)
        query = Q()
        if keyword_form.is_valid():
            keywords = keyword_form.cleaned_data["keywords"]
            for single_keyword in keywords.split(","):
                queryset = self.model_class.objects.filter(query)
        else:
            queryset = self.model_class.objects.all()

        f = self.get_filter_class()(self.request.GET, queryset=queryset)

        filter_query_set = f.qs

        for field in self.ajax_fields:
            if type(f.form.cleaned_data[field]) is list:
                # Multiple selection field
                if len(f.form.cleaned_data[field]) > 0:
                    exact_filter = {"%s__in" % field: f.form.cleaned_data[field]}
                else:
                    continue
            else:
                # Single select field
                if f.form.cleaned_data[field] is None:
                    continue
                exact_filter = {field: f.form.cleaned_data[field]}
            filter_query_set = filter_query_set.filter(**exact_filter)

        table = self.get_table_report_class()(filter_query_set)
        # table.paginate(page=request.GET.get('page', 1), per_page=5)
        # RequestConfig(request, paginate={"per_page": 5}).configure(table)
        self.table_to_report = RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        admin_base_url = self.get_admin_url()
        return {"table": table, "filter": f, "admin_base_url": admin_base_url}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not (self.table_to_report is None):
            return create_report_http_response(self.table_to_report, self.request)
        return self.render_to_response(context)

    def get_admin_url(self):
        content_type = ContentType.objects.get_for_model(self.model_class)
        url_name = "%s:%s_%s_change" % (self.edit_namespace, content_type.app_label, content_type.model)
        url = urlresolvers.reverse(url_name, args=("1",))
        url = url.replace("1", "%d")
        return url
