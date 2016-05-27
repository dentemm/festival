from django.conf.urls import url
from django.contrib.contenttypes.views import shortcut

from .views import custom_submit


urlpatterns = [
    url(r'^post/$', custom_submit, name='comments-post-comment'),
]