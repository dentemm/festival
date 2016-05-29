from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.wagtailcore import urls as wagtail_urls

from search import views as search_views


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    # python-social-auth
    url('', include('social.apps.django_app.urls', namespace='social')),
    #url(r'^home/$', 'festivaluser.views.login'),
    url(r'^user/', include('festivaluser.urls')),

    url(r'^search/$', search_views.search, name='search'),

    # third party applications
   # url(r'^comments/', include('django_comments.urls')),
    url(r'^comments/', include('comments.urls')),
    url(r'^ratings/', include('ratings.urls')),

    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.views.generic import TemplateView

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
