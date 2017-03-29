from django.http import HttpResponseRedirect
from django.shortcuts import render

from Auth.models import UserProfile
from NewsPanel.models import News
from apartments.models import Apartment, Podezd
from django import forms
from django.contrib.auth.models import User

# Create your views here.
from tariff.models import Tariffs, Utilities


class UID(forms.Form):
    uud = forms.UUIDField(label='Приглашение от главы ОСББ')




def NewsUser(request):
    usr = User.objects.get(podezd__level__apartment__userprofile__user=request.user)

    news = News.objects.filter(usercreator=usr).order_by('-data')
    return render(request, "UserNews.html", {'news': news})




def panel(request):
    if Apartment.objects.filter(userprofile__user=request.user):
        a = Apartment.objects.get(userprofile__user=request.user)


        return render(request, "UserPanel.html",{'Apart':a})
    else:
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = UID(request.POST)
            # check whether it's valid:
            if form.is_valid():
                if Apartment.objects.filter(uid = form.cleaned_data['uud']):
                    ap =Apartment.objects.get(uid=form.cleaned_data['uud'])
                    ap.userprofile = UserProfile.objects.get(user = request.user)
                    ap.save()
                return HttpResponseRedirect('/UserPanel/')

                # if a GET (or any other method) we'll create a blank form
        else:
            form = UID()

        return render(request, "Wellcom.html", {'form': form})
