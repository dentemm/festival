from django.forms import ModelForm

from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.wagtailcore.models import Page

class FestivalPageForm(WagtailAdminPageForm):
    '''
    Custom WagtailAdminPageForm subklasse. Deze wordt gebruikt om extra field validation te integreren
    '''

    def clean(self):
        cleaned_data = super(FestivalPageForm, self).clean()

        print(cleaned_data)


        '''rateable_attributes = cleaned_data.get('rateable_attributes')

        if len(rateable_attributes) != len(set(rateable_attributes)):

            msg = 'Een festival kan geen twee dezelfde te beoordelen attributen hebben'
            self.add_error('rateable_attributes', msg)'''


        print('CLEAN THIS SHIT')

        return cleaned_data

class MyModelForm(WagtailAdminModelForm):

    print('!!!!!!!!!!!------------!!!!!!!!!!!!')

    def clean(self):

        print('hhhhehehhehgqgmfqzgblzemnazgnam')

        return super(MyModelForm, self).clean()


class TestForm(WagtailAdminPageForm):

    def clean(self):
        cleaned_data = super(TestForm, self).clean()


        print('-------clean---------')
        print(cleaned_data)

        return cleaned_data