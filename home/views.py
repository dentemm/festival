import csv

from django.http import HttpResponse
from django import views

from .models import FestivalPage

def databaseExtractView(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="allefestivaladvisorusers.csv"'

	writer = csv.writer(response)

	writer.writerow(['festival_naam', 'festival_beschrijving', 'festival_datum', 'festival_aantal_dagen', 'festival_website_url',
			'festival_afbeelding_url', 'festival_locatie_naam', 'festival_locatie_adres', 'festival_contact_naam', 'festival_contact_email', 'festival_contact_phone'])


	for festival in FestivalPage.objects.all():

		naam = festival.name
		beschrijving = festival.description
		datum = festival.date
		duur = festival.duration
		website = festival.website
		foto = festival.main_image.file.url
		locatie = festival.location.name
		adres = festival.location.address.street + ' ' + festival.location.address.number + ' ' + festival.location.address.postal_code + ' ' + festival.location.address.city + ', ' + festival.location.address.country
		contact = festival.contact_person.first_name + ' ' +  festival.contact_person.last_name
		email = festival.contact_person.email
		phone = festival.contact_person.phone

		writer.writerow([naam, beschrijving, datum, duur, website, foto, locatie, adres, contact, email, phone])

	return reponse


def csvView(request):

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="allefestivaladvisorusers.csv"'

	writer = csv.writer(response)

	for fest in FestivalPage.objects.all():

		if fest.location and fest.contact_person:

			writer.writerow([fest.name, fest.location.address.city, fest.contact_person.first_name, fest.contact_person.last_name, fest.contact_person.email, fest.contact_person.phone])

		elif fest.contact_person and not fest.location:

			writer.writerow([fest.name, '', fest.contact_person.first_name, fest.contact_person.last_name, fest.contact_person.email, fest.contact_person.phone])

	return response

def statsView(request):
	
	return HttpResponse(request)
