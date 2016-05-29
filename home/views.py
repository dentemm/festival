from django.shortcuts import render

from wagtail.wagtailcore.models import Page
from wagtail.wagtailsearch.models import Query

from .models import FestivalPage


def search(request):
    # Search
    search_query = request.GET.get('query', None)
    if search_query:
        search_results = FestivalPage.objects.live().search(search_query)

        # Log the query so Wagtail can suggest promoted results
        Query.get(search_query).add_hit()
    else:
        search_results = Page.objects.none()

    # Render template
    return render(request, 'home/search_results.html', {
        'search_query': search_query,
        'search_results': search_results,
    })
