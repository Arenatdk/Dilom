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
from tariff.views import *
from Vote.views import *
from apartments.views import *
from UserPanel.views import *
from NewsPanel.views import *
from UsetTariff.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', login, name='login'),
    url(r'^register/$', register, name='register'),

    url(r'^logout/$', logout, name='logout'),
    url(r'^account/$', index_page, name='home'),

    url(r'^vote/$', vote, name='vote'),
    url(r'^vote_add/$', vote_add, name='vote_add'),



    url(r'^news/$', news, name='news'),
    url(r'^news_add/$', news_add, name='news_add'),
    url(r'^news_del/(?P<pk>\d+)/$', news_del, name='news_del'),



    url(r'^UserPanel/$', panel, name='panel'),
    url(r'^UserTariff/(?P<month>[0-9]*)-(?P<year>[0-9]{4})/$', UserTariff, name='UserTariff'),
    url(r'^NewsUser/$', NewsUser, name='NewsUser'),




    url(r'^tariff/', tarif_page, name='tariff'),
    url(r'^tariff_add/', add_taritt, name='tariff_add'),
    url(r'^pattern_ajax/', pattern_ajax, name='pattern_ajax'),
    url(r'^tarPDF/', tarpdf, name='tarpdf'),

    url(r'^contribution/(?P<month>[0-9]*)-(?P<year>[0-9]{4})/$', contribution, name='contribution'),
    url(r'^addpaid/', addpaid, name='addpaid'),

    #apartament
    url(r'^apartment/$', apartments, name='apartment'),
    url(r'^AddPodezd/$', AddPodezdPOST, name='AddPodezdPOST'),
    url(r'^AddLevel/$', AddLevelPOST, name='AddLevelPOST'),
    url(r'^enableTarif/$', enableTarif, name='enableTarif'),
    url(r'^DialogAddApartment/$', DialogAddApartment, name='DialogAddApartment'),
    url(r'^apartment/addUser/$', ApartamentAddUser, name='apartamentAddUser'),
    url(r'^apartment/(?P<pk>\d+)/edit/$', editApartament, name='editapartament')
]
