import django_tables2 as tables


class TableGeneratorColumn(object):
    def __init__(self):
        super(TableGeneratorColumn, self).__init__()
        self.column_title = None
        self.attrs = {'th': {"class": "hidden_header"}}
        self.column_content_template = '{{ record.id }}'

    def get_config_descriptor(self):
        return {self.column_title: tables.TemplateColumn(
            self.column_content_template,  attrs={'th': {"class": "hidden_header"}}
        )}

