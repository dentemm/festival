from wagtail.wagtailadmin.forms import WagtailAdminPageForm
from wagtail.wagtailcore.models import Page

class FestivalPageForm(WagtailAdminPageForm):
    '''
    Custom WagtailAdminPageForm subklasse. Deze wordt gebruikt om extra field validation te integreren
    '''

    def clean(self):
        cleaned_data = super(FestivalPageForm, self).clean()

        print(cleaned_data)

        rateable_attributes = cleaned_data.get('rateable_attributes')

        if len(rateable_attributes) != len(set(rateable_attributes)):

            msg = 'Een festival kan geen twee dezelfde te beoordelen attributen hebben'
            self.add_error('rateable_attributes', msg)

        return cleaned_data


class TestForm(WagtailAdminPageForm):

    def clean(self):

        print('-------clean---------')

        return super(TestForm, self).clean()