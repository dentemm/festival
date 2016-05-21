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

			address_string = address.street + ' ' + address.number + ' ' + address.postal_code + ' ' + address.city + ' ' + str(address.country.name)

			loc = geolocator.geocode(address_string)

			if isinstance(loc, geopy.location.Location):

				location.latitude = loc.latitude
				location.longitude = loc.longitude

				location.save()

		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))

