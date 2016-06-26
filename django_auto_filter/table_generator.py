from django_tables2_reports.tables import TableReport
import django_tables2 as tables
from tagging_app.tagging_app_utils import get_tag_str_from_tag_list


def render_tags(self, value):
    return get_tag_str_from_tag_list(value)


class TableGenerator(object):
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

    def __init__(self, model_class):
        super(TableGenerator, self).__init__()
        self.model_class = model_class

    def get_table_from_queryset(self, queryset):
        return self.get_table_report_class()(queryset)

    def get_table_for_all(self):
        return self.get_table_report_class()(self.model_class.objects.all())

    def get_table_report_class(self):
        # content_type = ContentType.objects.get_for_model(self.model_class)
        table_report_meta_attr_dict = {
            "model": self.model_class,
            # "row_attrs": {
            #     # 'data-id': lambda record: record.pk
            #     "objectId": lambda record: record.pk,
            #     "tags": lambda record: record.tags,
            #     "content-type": lambda record: ContentType.objects.get_for_model(record).pk,
            #     "data-name": "tags",
            # }
        }
        if self.is_tag_exists():
            table_report_meta_attr_dict["sequence"] = ["id", "tags"]
            table_report_meta_attr_dict["attrs"] = {
                # "data-show-toggle": "true",
                "data-show-columns": "true"
            }
        table_report_attr_dict = {
            "Meta": type("Meta", (), table_report_meta_attr_dict),

            # "edit": tables.Column(),
            # "render_edit":
            # "edit": tables.LinkColumn("admin:%s_%s_change" %
            #                           (content_type.app_label, content_type.model), args=[A('pk')])

        }
        if self.is_tag_exists():
            table_report_attr_dict.update(self.additional_col)
        table_class = type(self.model_class.__name__ + "AutoTable", (TableReport,), table_report_attr_dict)
        return table_class

    def is_tag_exists(self):
        all_objects = self.model_class.objects.all()
        if all_objects.exists():
            if hasattr(all_objects[0], "tags"):
                return True
        return False
