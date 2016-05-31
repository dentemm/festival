from django.conf.urls import url

from .views import RatingView, TestView, FormSetView


urlpatterns = [
    url(r'^rate/$', TestView.as_view(), name='rating'),
    url(r'^test/$', FormSetView.as_view(), name='formset')
]