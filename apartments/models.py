import uuid

from django.db import models
from django.contrib.auth.models import User
from Auth.models import UserProfile

# Create your models here.

class Podezd(models.Model):
    user = models.ForeignKey(User)
    numder = models.CharField(max_length=10)
    note = models.CharField(max_length=25)

    def __str__(self):
        return str(self.numder)


class Level(models.Model):
    podezd = models.ForeignKey(Podezd)
    level_number = models.IntegerField()
    def __str__(self):
        return str(self.level_number)+' id '+ str(self.id)


class subsidyi(models.Model):
    name = models.CharField(max_length=120)
    percent = models.IntegerField(blank=True, default=0)

class Apartment(models.Model ):
    level = models.ForeignKey(Level, null=True)
    numeber = models.CharField(max_length=10)
    userprofile = models.ForeignKey(UserProfile, null=True)
    countResidents = models.IntegerField(default=0)
    countRooms = models.IntegerField(default=0)
    area = models.IntegerField(default=0)
    HotArea  = models.IntegerField(default=0)
    isRent = models.BooleanField(default=False, verbose_name='В аренде')
    subsidyi = models.ForeignKey(subsidyi,null=True,blank=True)
    uid =  models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.numeber
