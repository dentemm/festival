from django.conf.urls import url

from .views import RatingView, TestView, FormSetView, csvRatings


urlpatterns = [
    url(r'^rate/$', TestView.as_view(), name='rating'),
    url(r'^test/$', FormSetView.as_view(), name='formset'),

    # CSV report about user ratings
    url(r'^report/$', csvRatings, name='report'),
   
]