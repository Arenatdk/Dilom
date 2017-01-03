"""Dilom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Auth.views import *
from ViewPage.views import *
from Vote.views import *
from apartments.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login, name='login'),
    url(r'^register/$', register, name='register'),

    url(r'^logout/$', logout, name='logout'),
    url(r'^account/$', index_page, name='home'),
    url(r'^vote/$', vote, name='vote'),
    url(r'^tariff/', tarif_page, name='tariff'),
    url(r'^tariff_add/', add_taritt, name='tariff_add'),


    #apartament
    url(r'^apartment/$', apartments, name='apartment'),
    url(r'^AddPodezd/$', AddPodezdPOST, name='AddPodezdPOST'),
    url(r'^AddLevel/$', AddLevelPOST, name='AddLevelPOST'),
    url(r'^DialogAddApartment/$', DialogAddApartment, name='DialogAddApartment'),
    url(r'^apartment/(?P<pk>\d+)/edit/$', editApartament, name='editapartament')
]
