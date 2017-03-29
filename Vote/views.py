from django.forms import forms
from django.shortcuts import render
from tariff.models import *
from django.http import HttpResponseRedirect
# Create your views here.

def vote(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request,"vote.html")


def vote_add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request,"vote_add.html")
