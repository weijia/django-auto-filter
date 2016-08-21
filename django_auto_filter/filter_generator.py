import django_filters
from ajax_select import make_ajax_form
from django import forms
from django.db.models import Q, BooleanField, NullBooleanField
from django.db import models

from djangoautoconf.ajax_select_utils.ajax_select_channel_generator import get_fields_with_icontains_filter
from djangoautoconf.model_utils.model_attr_utils import enum_model_fields
from django.utils.translation import ugettext_lazy as _


def is_int_field(attr):
    return type(attr) in [models.IntegerField, models.PositiveIntegerField, models.PositiveSmallIntegerField,
                          models.SmallIntegerField, models.BigIntegerField]


def is_bool_field(attr):
    return type(attr) in [BooleanField, NullBooleanField]


class FilterGenerator(object):
    def __init__(self, model_class, keyword_filter_fields=None):
        self.text_fields = {}
        super(FilterGenerator, self).__init__()
        self.model_class = model_class
        self.choice_fields = {}
        self.ajax_form = None
        self.keyword_filter_fields = keyword_filter_fields or get_fields_with_icontains_filter(model_class)
        # self.keyword_filter_fields = ['username', ]
        self.filter_instance = None
        self.ajax_fields = {}
        self.is_exclude_field_types = True
        self.default_exclude_fields = (models.ForeignKey, models.ManyToManyField, models.DateTimeField)

    def get_filter_instance(self, get_param):
        if self.filter_instance is None:
            self.filter_instance = self._get_filter_instance(get_param)
        return self.filter_instance

    def _get_filter_instance(self, get_param):
        keyword_form = self.get_contains_all_keyword_form()(get_param)
        query = Q()
        if keyword_form.is_valid():
            keywords = keyword_form.cleaned_data["keywords"]
            for single_keyword in keywords.split(","):
                if single_keyword == "":
                    continue
                for keyword_filter_field in self.keyword_filter_fields:
                    keyword_filter = {"%s__icontains" % keyword_filter_field: single_keyword}
                    query &= Q(**keyword_filter)
            queryset = self.model_class.objects.filter(query)
        else:
            queryset = self.model_class.objects.all()
        filter_instance = self.get_filter_class()(get_param, queryset=queryset)
        return filter_instance

    def set_ajax_form(self):
        self.ajax_form = make_ajax_form(self.model_class, self.ajax_fields, self.get_contains_all_keyword_form())
        for field in self.ajax_form.declared_fields:
            self.ajax_form.declared_fields[field].required = False

    def set_fields(self):
        for attr in enum_model_fields(self.model_class):
            if attr.name not in self.ajax_fields:
                if hasattr(attr, "choices") and len(attr.choices):
                    self.choice_fields[attr.name] = django_filters.MultipleChoiceFilter(choices=attr.choices)
                elif self.is_exclude_field_types:
                    if self.is_exclude_in_filter(attr):
                        continue
                    if is_bool_field(attr) or is_int_field(attr):
                        self.text_fields[attr.name] = ["exact"]
                    else:
                        self.text_fields[attr.name] = ["icontains"]

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

    def get_contains_all_keyword_form(self):
        form_class = type(self.model_class.__name__ + "ContainAllKeywordForm", (forms.ModelForm,), {
            "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
            _("keywords"): forms.CharField(required=False),
        })
        return form_class

    def is_exclude_in_filter(self, attr):
        field_types = self.get_excluded_field_types()
        if type(attr) in field_types:
            return True
        for field_type in field_types:
            if issubclass(type(attr), field_type):
                return True
        return False

    def get_excluded_field_types(self):
        excluded_types = list(self.default_exclude_fields)
        try:
            # noinspection PyUnresolvedReferences
            from mptt.models import TreeForeignKey
            excluded_types.append(TreeForeignKey)
        except ImportError:
            pass
        return excluded_types

    def get_contains_all_keyword_form(self):
        form_class = type(self.model_class.__name__ + "ContainAllKeywordForm", (forms.ModelForm,), {
            "Meta": type("Meta", (), {"model": self.model_class, "fields": []}),
            "keywords": forms.CharField(required=False),
        })
        return form_class

    def get_query_set(self, get_param):
        filter_query_set = self.get_filter_instance(get_param).qs
        for field in self.ajax_fields:
            if type(self.filter_instance.form.cleaned_data[field]) is list:
                # Multiple selection field
                if len(self.filter_instance.form.cleaned_data[field]) > 0:
                    exact_filter = {"%s__in" % field: self.filter_instance.form.cleaned_data[field]}
                else:
                    continue
            else:
                # Single select field
                if self.filter_instance.form.cleaned_data[field] is None:
                    continue
                exact_filter = {field: self.filter_instance.form.cleaned_data[field]}
            filter_query_set = filter_query_set.filter(**exact_filter)
        return filter_query_set
