import django_tables2 as tables

from django_auto_filter.table_generator_column import TableGeneratorColumn
from tagging_app.tagging_app_utils import get_tag_str_from_tag_list


def render_tags(self, value):
    return get_tag_str_from_tag_list(value)


# The following line make the column editable (work for x editable)
class TagColumn(object):
    # noinspection PyMethodMayBeStatic
    def get_config_descriptor(self):
        return {"tags": tables.Column(attrs={'th': {"data-editable": "true"}})}


class RowInfoColumn(TableGeneratorColumn):
    def __init__(self):
        super(RowInfoColumn, self).__init__()
        self.column_title = "row_info"
        self.attrs = {'th': {"class": "hidden-column"},
                      "td": {"class": "hidden-column"}}
        self.column_content_template = '<span {{ record|gen_tag_attr }}> </span>'


class TagRender(object):
    # noinspection PyMethodMayBeStatic
    def get_config_descriptor(self):
        {"render_tags": render_tags}
