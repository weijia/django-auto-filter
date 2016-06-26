# dynamic_preferences_registry.py

from dynamic_preferences.types import BooleanPreference, StringPreference, Section
from dynamic_preferences.registries import user_preferences_registry, global_preferences_registry

# we create some section objects to link related preferences together

# general = Section('general')
discussion = Section('discussion')


# # We start with a global preference
# @global_preferences_registry.register
# class SiteTitle(StringPreference):
#     section = general
#     name = 'title'
#     default = 'My site'
#
#
# @global_preferences_registry.register
# class MaintenanceMode(BooleanPreference):
#     name = 'maintenance_mode'
#     default = False


# now we declare a per-user preference
@user_preferences_registry.register
class CommentNotificationsEnabled(BooleanPreference):
    """Do you want to be notified on comment publication ?"""
    section = discussion
    name = 'comment_notifications_enabled'
    default = True
