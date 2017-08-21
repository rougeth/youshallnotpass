from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^logout/$', auth_views.logout, name='account_logout'),
    url(r'^', include('social_django.urls', namespace='social')),
]
