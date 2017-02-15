from asyncio import selector_events

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.base_user import AbstractBaseUser




class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True)
    isOSMD =models.BooleanField(default=False, verbose_name='Является ОСМД')
    FirstName = models.CharField(max_length=30, verbose_name='Имя')
    LastName = models.CharField(max_length=30, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=30, verbose_name='Отчество')
    number = models.CharField(max_length=20, verbose_name='Номер телефона')
    OSBBname = models.CharField(blank=True, max_length=50, verbose_name='Название OSBB')
    addres = models.CharField(blank=True, max_length=50, verbose_name='Город')
    street = models.CharField(blank=True, max_length=50, verbose_name='Улица')
    homenumber = models.CharField(blank=True, max_length=10, verbose_name='Номер дома')




        # avatar = models.ImageField(upload_to='images/users', verbose_name='Изображение')


    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

def user_post_save(sender, instance, **kwargs):
    ( profile, new ) = UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)


