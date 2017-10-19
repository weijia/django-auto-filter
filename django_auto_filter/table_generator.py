from django_tables2_reports.tables import TableReport
try:
    from django_auto_filter.tag_column import RowInfoColumn, TagColumn
    from tagging_app.tagging_app_utils import get_tag_str_from_tag_list
except:
    pass


def render_tags(self, value):
    return get_tag_str_from_tag_list(value)


class TableGenerator(object):
    def __init__(self, model_class, prefix=None):
        super(TableGenerator, self).__init__()
        self.model_class = model_class
        self.report_meta_attr_dict = {
            "model": self.model_class,
        }
        self.additional_column = None
        self.report_attr_dict = None
        self.exclude = None
        self.prefix = prefix
        self.table_column_config_list = []

    def get_table_from_queryset(self, queryset):
        table_create_dict = {"data": queryset}
        if self.prefix is not None:
            table_create_dict["prefix"] = self.prefix
        if self.exclude is not None:
            table_create_dict["exclude"] = self.exclude
        return self.get_table_report_class()(**table_create_dict)

    def get_table_for_all(self):
        return self.get_table_from_queryset(self.model_class.objects.all())

    def get_table_report_class(self):
        """
        Generate the following table class:
        class XxxxxAutoTable(TableReport):
            class Meta:
                model = Xxxxx
                exclude = []
        :return:
        """
        self.report_attr_dict = {}

        # content_type = ContentType.objects.get_for_model(self.model_class)
        self.add_tag_column_if_exists()

        if self.additional_column:
            self.report_attr_dict.update(self.additional_column)

        if len(self.table_column_config_list) > 0:
            for column_config in self.table_column_config_list:
                self.report_attr_dict.update(column_config.get_config_descriptor())

        self.add_column_selector()

        self.report_attr_dict.update({
            "Meta": type("Meta", (), self.report_meta_attr_dict),
        })

        table_class = type(self.model_class.__name__ + "AutoTable", (TableReport,), self.report_attr_dict)
        return table_class

    def add_tag_column_if_exists(self):
        if self.is_tag_exists():
            self.put_tag_behind_id_column()
            self.report_attr_dict.update()
            self.table_column_config_list.append(TagColumn())
            self.table_column_config_list.append(RowInfoColumn())

    def put_tag_behind_id_column(self):
        self.report_meta_attr_dict["sequence"] = ["id", "tags"]

    def add_column_selector(self):
        self.report_meta_attr_dict["attrs"] = {
            # "data-show-toggle": "true",
            "data-show-columns": "true"
        }

    def is_tag_exists(self):
        try:
            from django_auto_filter.tag_column import RowInfoColumn, TagColumn
        except:
            return False
        all_objects = self.model_class.objects.all()
        if all_objects.exists():
            if hasattr(all_objects[0], "tags"):
                return True
        return False
