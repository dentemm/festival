import django
from django import forms
from django.forms.models import fields_for_model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import EditHandler, FieldPanel, MultiFieldPanel
from wagtail.wagtailadmin.forms import formfield_for_dbfield

def extract_panel_definitions_from_model_class(model, exclude=None):
    if hasattr(model, 'panels'):
        return model.panels

    panels = []

    _exclude = []
    if exclude:
        _exclude.extend(exclude)

    fields = fields_for_model(model, exclude=_exclude, formfield_callback=formfield_for_dbfield)

    for field_name, field in fields.items():
        try:
            panel_class = field.widget.get_panel()
        except AttributeError:
            panel_class = FieldPanel

        panel = panel_class(field_name)
        panels.append(panel)

    return panels

def widget_with_script(widget, script):
    return mark_safe('{0}<script>{1}</script>'.format(widget, script))


class BaseCustomInlinePanel(EditHandler):
    @classmethod
    def get_panel_definitions(cls):
        # Look for a panels definition in the InlinePanel declaration
        if cls.panels is not None:
            return cls.panels
        # Failing that, get it from the model
        else:
            return extract_panel_definitions_from_model_class(
                cls.related.related_model,
                exclude=[cls.related.field.name]
            )

    _child_edit_handler_class = None

    @classmethod
    def get_child_edit_handler_class(cls):
        if cls._child_edit_handler_class is None:
            panels = cls.get_panel_definitions()
            cls._child_edit_handler_class = MultiFieldPanel(
                panels,
                heading=cls.heading
            ).bind_to_model(cls.related.related_model)

        return cls._child_edit_handler_class

    @classmethod
    def required_formsets(cls):
        child_edit_handler_class = cls.get_child_edit_handler_class()
        return {
            cls.relation_name: {
                'fields': child_edit_handler_class.required_fields(),
                'widgets': child_edit_handler_class.widget_overrides(),
                'min_num': cls.min_num,
                'validate_min': cls.min_num is not None,
                'max_num': cls.max_num,
                'validate_max': cls.max_num is not None
            }
        }

    def __init__(self, instance=None, form=None):
        super(BaseCustomInlinePanel, self).__init__(instance=instance, form=form)

        self.formset = form.formsets[self.__class__.relation_name]

        child_edit_handler_class = self.__class__.get_child_edit_handler_class()
        self.children = []
        for subform in self.formset.forms:
            # override the DELETE field to have a hidden input
            subform.fields['DELETE'].widget = forms.HiddenInput()

            # ditto for the ORDER field, if present
            if self.formset.can_order:
                subform.fields['ORDER'].widget = forms.HiddenInput()

            self.children.append(
                child_edit_handler_class(instance=subform.instance, form=subform)
            )

        # if this formset is valid, it may have been re-ordered; respect that
        # in case the parent form errored and we need to re-render
        if self.formset.can_order and self.formset.is_valid():
            self.children = sorted(self.children, key=lambda x: x.form.cleaned_data['ORDER'])

        empty_form = self.formset.empty_form
        empty_form.fields['DELETE'].widget = forms.HiddenInput()
        if self.formset.can_order:
            empty_form.fields['ORDER'].widget = forms.HiddenInput()

        self.empty_child = child_edit_handler_class(instance=empty_form.instance, form=empty_form)

    template = "home/custom_panels/custom_inline_panel.html"

    def render(self):
        formset = render_to_string(self.template, {
            'self': self,
            'can_order': self.formset.can_order,
        })
        js = self.render_js_init()
        return widget_with_script(formset, js)

    js_template = "wagtailadmin/edit_handlers/inline_panel.js"

    def render_js_init(self):
        return mark_safe(render_to_string(self.js_template, {
            'self': self,
            'can_order': self.formset.can_order,
        }))


class CustomInlinePanel(object):

    def __init__(self, relation_name, panels=None, label='', help_text='', min_num=None, max_num=None):

        self.relation_name = relation_name
        self.panels = panels
        self.label = label
        self.help_text = help_text
        self.min_num = min_num
        self.max_num = max_num

    @property
    def test(self):

        print('jeeeeeeeeeeeeeeeeeeeeeeeeeeej')

        return 'jeeeeeeeeeeeeeeeeeeeeeeeeeeej'


    def bind_to_model(self, model):

        if django.VERSION >= (1, 9):
            related = getattr(model, self.relation_name).rel

        else:
            related = getattr(model, self.relation_name).related

        return type(str('_CustomInlinePanel'), (BaseCustomInlinePanel, ), {
            'model': model,
            'relation_name': self.relation_name,
            'related': related,
            'panels': self.panels,
            'heading': self.label,
            'help_text': self.help_text,
            'min_num': self.min_num,
            'max_num': self.max_num
        })

    

