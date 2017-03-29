from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class  News(models.Model):
    usercreator = models.ForeignKey(User)
    name = models.CharField(max_length=25)
    text = models.TextField()
    data = models.DateTimeField()