from glob import glob
from importlib import import_module
from pathlib import Path

from django.conf import settings
from django.template import Library, Template
from django.utils.text import slugify

from docstring_parser import parse, ParseError

from calico.templatetags.calico import DocStringNode
from yak.tags import TemplateTag


register = Library()


class AddWidgetsListToContext(TemplateTag):

    def get_installed_apps_dirs(self):
        for app in settings.INSTALLED_APPS:
            module = import_module(app)
            yield (app, Path(module.__file__).parent)

    def get_widgets_for_dir(self, path):
        return glob('**/*.html', root_dir=path / 'templates' / 'widgets', recursive=True)

    def get_all_widgets(self):
        widgets = {}
        for app, path in self.get_installed_apps_dirs():
            for widget in self.get_widgets_for_dir(path):
                if widget in widgets:
                    widgets[widget][1].append(app)
                else:
                    widgets[widget] = (path, [app])

        return widgets

    def render(self, context, as_var='widgets'):
        print('called')
        context[as_var] = sorted(self.get_all_widgets().items())
        from pprint import pprint
        pprint(context[as_var])
        context['section']['anchors'] = {
            widget_anchor(p): widget_name(p)
            for p in context[as_var]
        }
        return ''


register.tag('add_widgets_list_to_context', AddWidgetsListToContext.as_tag())


class WidgetDocString(TemplateTag):
    template_name = 'calico_widget_docs/docstring.html'

    def get_widget_doc_string(self, app_path, widget_path):
        with open(Path(app_path) / 'templates' / 'widgets' / widget_path) as f:
            t_string = f.read()
        template = Template(t_string)

        for node in template.nodelist:
            if isinstance(node, DocStringNode) and node.doc_string:
                return node.doc_string

    def render(self, app_path, widget_path):
        docstring = None
        error = None
        try:
            ds = self.get_widget_doc_string(app_path, widget_path)
            if ds:
                docstring = parse(ds)
            else:
                error = 'No documentation found'
        except ParseError as e:
            error = e

        return {
            'docstring': docstring,
            'error': error
        }


register.tag('doc_string', WidgetDocString.as_tag())


@register.filter
def widget_name(widget_pair):
    return widget_pair[0].rsplit('.html', 1)[0].replace('/', '.')


@register.filter
def widget_anchor(widget_pair):
    return slugify(widget_pair[0].rsplit('.html', 1)[0])
