from django_tables2_reports.tables import TableReport
import django_tables2 as tables
from tagging_app.tagging_app_utils import get_tag_str_from_tag_list


def render_tags(self, value):
    return get_tag_str_from_tag_list(value)


class TableGenerator(object):
    tag_cols = {
        # The following line make the column editable (work for x editable)
        "tags": tables.Column(attrs={'th': {"data-editable": "true"}}),
        "render_tags": render_tags,
        "row_info": tables.TemplateColumn('<span {{ record|gen_tag_attr }}> </span>',
                                          # Hide this column
                                          attrs={'th': {"class": "hidden-column"},
                                                 "td": {"class": "hidden-column"}},
                                          ),
    }

    def __init__(self, model_class):
        super(TableGenerator, self).__init__()
        self.model_class = model_class
        self.report_meta_attr_dict = {
            "model": self.model_class,
        }
        self.additional_column = None
        self.report_attr_dict = None
        self.exclude = None

    def get_table_from_queryset(self, queryset):
        return self.get_table_report_class()(queryset)

    def get_table_for_all(self):
        return self.get_table_report_class()(self.model_class.objects.all(), exclude=self.exclude)

    def get_table_report_class(self):
        # content_type = ContentType.objects.get_for_model(self.model_class)
        if self.is_tag_exists():
            self.add_tag_column()
        self.report_attr_dict = {
            "Meta": type("Meta", (), self.report_meta_attr_dict),
        }
        if self.is_tag_exists():
            self.report_attr_dict.update(self.tag_cols)

        if self.additional_column:
            self.report_attr_dict.update(self.additional_column)

        table_class = type(self.model_class.__name__ + "AutoTable", (TableReport,), self.report_attr_dict)
        return table_class

    def add_tag_column(self):
        self.report_meta_attr_dict["sequence"] = ["id", "tags"]
        self.report_meta_attr_dict["attrs"] = {
            # "data-show-toggle": "true",
            "data-show-columns": "true"
        }

    def is_tag_exists(self):
        all_objects = self.model_class.objects.all()
        if all_objects.exists():
            if hasattr(all_objects[0], "tags"):
                return True
        return False
