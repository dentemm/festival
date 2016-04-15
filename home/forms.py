from django.forms import ModelForm

from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.wagtailcore.models import Page


class AddressForm(ModelForm):

    def clean(self):

        print('---- Address Form clean() methode')
        return super(AddressForm, self).clean()


