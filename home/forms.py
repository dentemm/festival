from django.forms import ModelForm

from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.wagtailcore.models import Page



class AddressForm(ModelForm):

    def clean(self):

        print('---- Address Form clean() methode')
        return super(AddressForm, self).clean()


class FestivalPageForm(WagtailAdminPageForm):
    '''
    Custom WagtailAdminPageForm subklasse. Deze wordt gebruikt om extra field validation te integreren
    '''

    def clean(self):
        cleaned_data = super(FestivalPageForm, self).clean()



        print('Festival Page Form clean() methode')
        print(cleaned_data)
        print('page: %s' % self.instance)

        page = self.instance

        print('page persons: %s' % page.persons)

        return cleaned_data