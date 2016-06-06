from ufs_tools import get_folder, os
from ufs_tools.string_tools import class_name_to_low_case


def get_model_app(model_class):
    # app_folder = os.path.dirname(get_folder(model_class.__file__))
    # name = os.path.basename(app_folder)
    return model_class._meta.app_label
    # return name


def get_rest_api_url(model_class):
    rest_api_url = "/%s/rest_api/%s/" % (get_model_app(model_class), class_name_to_low_case(model_class.__name__))
    return rest_api_url
