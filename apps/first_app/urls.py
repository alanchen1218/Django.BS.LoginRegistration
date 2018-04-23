from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),  # anything that comes in goes to index then the others
    url(r'register$', views.register), 
    url(r'login$', views.login),
    url(r'success$', views.success),
    url(r'home$', views.home),
    url(r'logout$', views.logout),
    url(r'addBook$', views.addBook),
    url(r'^createReview/(?P<number>\d+)$', views.createReview),
    url(r'^show/(?P<number>\d+)$', views.show),
    url(r'^user/(?P<number>\d+)$', views.user),
    url(r'^destroy/(?P<number>\d+)$', views.destroy),
]  