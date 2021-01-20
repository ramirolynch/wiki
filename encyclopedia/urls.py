from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"), 
    path('wiki/<str:entry>', views.entry, name="entry"),
    path('new', views.new, name="new"),
    path('wiki/<str:entry>/edit', views.edit, name="edit"),
    path('rdm', views.rdm, name="rdm"), 
    path('search', views.search, name="search"),

]
