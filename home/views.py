import csv

from django.http import HttpResponse

from .models import FestivalPage


def csvView(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="allefestivaladvisorusers.csv"'

	writer = csv.writer(response)

	for fest in FestivalPage.objects.all():

		writer.writerow([fest.name, fest.location.address.city, fest.contact_person.first_name, fest.contact_person.last_name, fest.contact_person.email, fest.contact_person.phone])

	return response

