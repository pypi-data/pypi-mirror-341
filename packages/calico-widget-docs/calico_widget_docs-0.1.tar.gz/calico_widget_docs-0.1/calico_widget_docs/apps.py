from django.apps import AppConfig

from calico import hook


class CalicoWidgetDocsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calico_widget_docs'


# # Only use one of those
# # a theme automatically gets added to installed apps
# # using both would mean having the installed app twice
@hook
# def declare_theme():
def installed_apps():
    return ['calico_widget_docs']



# @hook
# def calico_css(theme):
#     pass



# @hook
# def calico_js(theme):
#     pass


# @hook
# def site_groupings():
#     pass


@hook
def auto_load_tags():
    return ['calico_widget_docs.templatetags.widget_docs']


# @hook
# def calico_defaults():
#     pass

