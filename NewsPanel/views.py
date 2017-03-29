from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.utils.timezone import now

from NewsPanel.models import News

# Create your views here.

def news(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    news = News.objects.filter(usercreator=request.user).order_by('-data')
    return render(request,"News.html", {'news': news})


class add_newsForm(forms.Form):

    name = forms.CharField(max_length=25,widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea'}))

def news_del(request,pk):
    nw = News.objects.get(id=pk)
    nw.delete()
    return HttpResponseRedirect('/news/')

def news_add(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = add_newsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            NW = News()
            NW.usercreator = request.user
            NW.name = form.cleaned_data['name']
            NW.text = form.cleaned_data['text']
            NW.data = now()
            NW.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/news/')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = add_newsForm()

    return render(request, 'news_add.html', {'form': form})



