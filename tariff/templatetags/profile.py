from django.contrib.auth.models import User

from django import template

register = template.Library()

@register.tag
def current_user(test):
    return User.objects.get(username=test).userprofile.LastName