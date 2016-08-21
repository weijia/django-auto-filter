import django_tables2 as tables


class TableGeneratorColumn(object):
    column_content_template = '{{ record.id }}'
    column_title = None
    attributes = {'th': {"class": "hidden_header"}}

    def get_config_descriptor(self):
        return {self.column_title: tables.TemplateColumn(
            self.column_content_template,  attrs=self.attributes
        )}

