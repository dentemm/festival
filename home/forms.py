from django.forms import ModelForm

from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.wagtailcore.models import Page

from .models import FestivalPageRateableAttributeValue


class AddressForm(ModelForm):

    def clean(self):
        print('---- Address Form clean() methode')
        return super(AddressForm, self).clean()


FestivalPageRatebleAttributeValueForm(WagtailAdminModelForm):

    def get_initial(self):
		
        try: 
            return FestivalPageRateableAttributeValue.objects.get(id=self.initial['name']).name
		
        except:
            return None
