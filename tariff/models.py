# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from Auth.models import UserProfile
from apartments.models import Apartment

class Tariff_type(models.Model):
    type_name= models.CharField(max_length=120)
    def __str__(self):
        return (self.type_name)

class Tariffs(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    unit_measure = models.CharField(max_length=15, blank=True)
    enable = models.BooleanField(default=True)
    type = models.ForeignKey(Tariff_type)
    price0_t1 = models.FloatField(max_length=20, blank=True , default=0)
    price0_t2 = models.FloatField(max_length=20, blank=True , default=0)

    benefit0_t1 = models.BooleanField(default=False, verbose_name='Льгота')
    benefit0_t2 = models.BooleanField(default=False, verbose_name='Льгота')
    level1_t1 = models.FloatField(max_length=15,blank=True, default=0)
    level1_t2 = models.FloatField(max_length=15,blank=True, default=0)
    price1_t1 = models.FloatField(max_length=20, blank=True, default=0)
    price1_t2 = models.FloatField(max_length=20, blank=True, default=0)

    benefit1_t1 = models.BooleanField(default=False, verbose_name='Льгота')
    benefit1_t2 = models.BooleanField(default=False, verbose_name='Льгота')
    level2_t1 = models.FloatField(max_length=15,blank=True, default=0)
    level2_t2 = models.FloatField(max_length=15,blank=True, default=0)
    price2_t1 = models.FloatField(max_length=20, blank=True, default=0)
    price2_t2 = models.FloatField(max_length=20, blank=True, default=0)
    benefit2_t1 = models.BooleanField(default=False, verbose_name='Льгота')
    benefit2_t2 = models.BooleanField(default=False, verbose_name='Льгота')
    coment = models.TextField(max_length=100, blank=True, default="")
    residents = models.ManyToManyField(Apartment) #Связь с квартирами
    def __str__(self):
        return ( self.name)


class Patterns(models.Model):
    name = models.CharField(max_length=50)
    unit_measure = models.CharField(max_length=15, blank=True)
    type = models.ForeignKey(Tariff_type)

    def __str__(self):
        return (self.name)

class Utilities(models.Model):
        tarif = models.ForeignKey(Tariffs)
        apartment = models.ForeignKey(Apartment)
        previous_readings = models.FloatField(max_length=15, blank=True, default=0)
        current_raadings = models.FloatField(max_length=15, blank=True, default=0)
        previous_readings_c2 = models.FloatField(max_length=15, blank=True, default=0)
        current_raadings_c2 = models.FloatField(max_length=15, blank=True, default=0)
        paid = models.BooleanField(default=False)
        paid_date = models.DateField(null=True, blank=True)
        dateAdd = models.DateField()
        comment = models.CharField(max_length=15, blank=True)

        def __str__(self):
            return (self.comment)


class subsidy(models.Model):
    pass


