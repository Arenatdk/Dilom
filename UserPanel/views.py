from django.http import HttpResponseRedirect
from django.shortcuts import render

from Auth.models import UserProfile
from NewsPanel.models import News
from apartments.models import Apartment, Podezd
from django import forms
from django.contrib.auth.models import User

# Create your views here.
from tariff.models import Tariffs, Utilities
from django import forms
from django.contrib.auth.models import User

from django.db import models
from django.forms import ModelForm, Textarea, TextInput
from Auth.models import UserProfile
from tariff.views import sumFormula


class UID(forms.Form):
    uud = forms.UUIDField(label='Приглашение от главы ОСББ')




def NewsUser(request):
    usr = User.objects.get(podezd__level__apartment__userprofile__user=request.user)

    news = News.objects.filter(usercreator=usr).order_by('-data')
    return render(request, "UserNews.html", {'news': news})
import csv
from django.http import HttpResponse
def getreportforuser(request,pk):
    apart = Apartment.objects.get(id=pk)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Report.csv"'

    writer = csv.writer(response)
    writer.writerow([apart.userprofile.LastName, apart.userprofile.FirstName, apart.userprofile.patronymic])
    writer.writerow(['Обслуживает ОСМД: '+apart.level.podezd.user.userprofile.OSBBname,'Глава: '+ apart.level.podezd.user.userprofile.LastName + ' '+apart.level.podezd.user.userprofile.FirstName+ ' '+apart.level.podezd.user.userprofile.patronymic, 'Телефон: '+apart.level.podezd.user.userprofile.number])
    writer.writerow(['Адрес: '+str(apart.level.podezd.user.userprofile.addres)+', '+str(apart.level.podezd.user.userprofile.street)+' '+str(apart.level.podezd.user.userprofile.homenumber)+', № '+str(apart.numeber), 'подъезд '+str(apart.level.podezd.numder) +', этаж '+str(apart.level.level_number) ])
    writer.writerow(['Количество проживающих: '+str(apart.countResidents), 'Количество комнат: '+str(apart.countRooms), 'Общая площадь: '+str(apart.area) + ' м²', 'Отопительная площадь: '+str(apart.HotArea)+ ' м²'])

    writer.writerow([''])
    writer.writerow([''])
    writer.writerow(['Начисления'])
    writer.writerow(
        ['Услуга', 'Предыдущие показания', 'Текущие показания', 'Расчет стоймости', 'Сумма', 'Период', 'Оплачено'])
    tar = []
    apart = Apartment.objects.get(id = pk)
    for t in Tariffs.objects.filter(residents__id=pk):

        t.dat()
        t.apart = []
        tar.append(t)

        for ap in t.residents.filter(userprofile__user=request.user):
            ap.ut = []
            for util in Utilities.objects.filter( apartment=ap, tarif=t):
                sumFormula(t, util)
                ap.ut.append(util)
                writer.writerow([util.tarif.name,sort_prev(util),sort_cur(util),str(util.formula),str(util.sum),str(util.dateFirst)+'\n'+str(util.dateAdd),truetoyes(util.paid) ])
            t.apart.append(ap)



    return response
def sort_cur(utl):
    if utl.current_raadings == 0:
        return ''
    if utl.current_raadings_c2 == 0:
        return str(utl.current_raadings)+' '+utl.tarif.unit_measure

    return str(utl.current_raadings)+' '+utl.tarif.unit_measure+ ' '+ str(utl.current_raadings_c2)+' '+utl.tarif.unit_measure

def sort_prev(utl):
    if utl.previous_readings == 0:
        return ''
    if utl.previous_readings_c2 == 0:
        return str(utl.previous_readings)+' '+utl.tarif.unit_measure

    return str(utl.previous_readings)+' '+utl.tarif.unit_measure+ ' '+ str(utl.previous_readings_c2)+' '+utl.tarif.unit_measure

def truetoyes(t):
    if t:
        return 'Да'
    else:
        return 'Нет'

class formuser(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('FirstName','LastName','patronymic','number','OSBBname','addres','street','homenumber')
        widgets = {
            'FirstName': TextInput(attrs={'class': 'form-control'}),
            'LastName': TextInput(attrs={'class': 'form-control'}),
            'patronymic': TextInput(attrs={'class': 'form-control'}),
            'number': TextInput(attrs={'class': 'form-control'}),
            'OSBBname': TextInput(attrs={'class': 'form-control'}),
            'addres': TextInput(attrs={'class': 'form-control'}),
            'street': TextInput(attrs={'class': 'form-control'}),
            'homenumber': TextInput(attrs={'class': 'form-control'}),
        }

class passchang(forms.Form):

    pass1 = forms.CharField( required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}),
                            label="Новый пароль", min_length=6, max_length=30)
    pass2 = forms.CharField(required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль еще раз'}),
        label="Пароль ещё раз", min_length=6, max_length=30)

    def clean_pass2(self):
        if (len(self.cleaned_data["pass2"])==0):
            raise forms.ValidationError("Пусто")
        if (self.cleaned_data["pass2"] != self.cleaned_data.get("pass1", "")):
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data["pass2"]




def Settings(request):
    err=''
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = formuser(request.POST,instance=UserProfile.objects.get(user=request.user) )
        if form.is_valid():
            form.save()

        pssch = passchang(request.POST)
        err= 'Пароль не изменен'
        if pssch.is_valid():
            u = User.objects.get(username=request.user)
            u.set_password(pssch.cleaned_data["pass1"])
            u.save()
            err = 'Пароль изменен'
            print(pssch.cleaned_data["pass1"])

        # check whether it's valid:
    else:
        form = formuser(instance=UserProfile.objects.get(user=request.user))
        pssch = passchang()


    return render(request, "OsbbSettings.html",{'form':form,'passch':passchang, 'err':err})


def Settingsuser(request):
    pass

def panel(request):
    if Apartment.objects.filter(userprofile__user=request.user):
        a = Apartment.objects.get(userprofile__user=request.user)
        owner = UserProfile.objects.get(user = request.user)

        return render(request, "UserPanel.html",{'Apart':a,'owner':owner})
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
