from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.account, name='account'),
	url(r'login/$', views.login, name='login'),
	url(r'logout/$', views.logout, name='logout'),

	# tests
	url(r'test/$', views.UserProfileView.as_view(), name='test')
]