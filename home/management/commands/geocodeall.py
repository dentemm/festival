import geopy
#from geopy.geocoders import Nominatim

from django.core.management.base import BaseCommand, CommandError

from home.models import Address, Location

class Command(BaseCommand):

	help = 'Adds latitude and longitude properties for all Address objects'

	def handle(self, *args, **options):

		for location in Location.objects.all():

			address = location.address
			geolocator = geopy.geocoders.Nominatim()

			number = address.number 

			address_string = address.street + ' ' + address.number + ' ' + address.postal_code + ' ' + address.city + ' ' + str(address.country.name)

			loc = geolocator.geocode(address_string)

			if not isinstance(loc, geopy.location.Location):

				alternative = address.street + ' ' + address.postal_code + ' ' + address.city + ' ' + str(address.country.name)

				loc = geolocator.geocode(alternative)


			if isinstance(loc, geopy.location.Location):

				location.latitude = loc.latitude
				location.longitude = loc.longitude

				location.save()

			else:

				location.latitude = 50.8333;
				location.longitude = 4.0000;

				location.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))

