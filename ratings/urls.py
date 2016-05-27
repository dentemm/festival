from django.conf.urls import url

from .views import RatingView, TestView


urlpatterns = [
    url(r'^rate/$', TestView.as_view(), name='rating'),
]