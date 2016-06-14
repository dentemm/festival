from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
	url(r'^$', views.UserProfileView.as_view(), name='account'),
	#url(r'login/$', views.login, name='login'),
	url(r'login/$', views.login_user, name='test3'),
	url(r'logout/$', views.logout, name='logout'),

	url(r'test/$', auth_views.login),

	# tests
	url(r'test/$', views.UserProfileView.as_view(), name='test'),
	url(r'register/$', views.register_user, name='register'),

	# CSV file -- alle gebruikers
	url(r'allegebruikers/$', views.csvView, name='csv'),

]