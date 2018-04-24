from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),   # This line has changed! Notice that urlpatterns is a list, the comma is in
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    # url(r'^dashboard$', views.dashboard),
    # url(r'wish_items/create$', views.create),
    # url(r'^createrender$', views.createrender),

    # url(r'^wish_items/(?P<number>\d+)$', views.wishItem), # NOT WORKING

    # url(r'^destroy/(?P<number>\d+)$', views.destroy),
    # url(r'^add/(?P<number>\d+)$', views.add), NOT WORKING>>>>>>

]