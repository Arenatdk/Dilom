from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from .models import *
from collections import OrderedDict
from Auth.models import UserProfile
from tariff.models import Tariffs, subsidy


# Create your views here.
class AddPodezd(forms.Form):
    numder = forms.CharField(label='Номер',max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}))
    note = forms.CharField(label='Коментарий',max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))

class AddLevel(forms.Form):
    level_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))

class AddLevelForm(forms.Form):
    PodezdID= forms.IntegerField(widget = forms.HiddenInput())
    count_level = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))
#    start_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number'}))


def apartments(request):
    PodezdForm = AddPodezd()
    LevelForm= AddLevel()
    podezd =  Podezd.objects.filter(user=request.user)
    PodezdList = Podezd.objects.filter(user=request.user)
    levelList = Level.objects.filter(podezd__user=request.user).order_by('id').reverse()
    ApartmentList = Apartment.objects.filter(level__podezd__user=request.user).order_by('id')

    return render(request, "apartments.html", {'PodezdForm':PodezdForm, 'LevelForm':LevelForm, 'PodezdList':PodezdList,'podezd':podezd,'levelList':levelList,'ApartmentList':ApartmentList})

def AddPodezdPOST(request):
    if request.method == 'POST':
        #if request.POST.get('AddPodezd') is not None:
            PodezdForm = AddPodezd(request.POST)
            if PodezdForm.is_valid():
                podezd = Podezd()
                podezd.user = request.user
                podezd.numder =PodezdForm.cleaned_data['numder']
                podezd.note = PodezdForm.cleaned_data['note']
                podezd.save()
    return HttpResponseRedirect('/apartment/')

def AddLevelPOST(request):
    print(request.POST)
    if request.method == 'POST':

        countlevel = int(request.POST.get('LevelNumberInput'))
        podezdID = request.POST.get('PodezdNameAddLevel')
        i = 1
        print(countlevel)
        while i<=countlevel:
            print(i)
            l= Level()
            l.podezd_id=podezdID
            l.level_number= i
            l.save()
            i+=1

    return HttpResponseRedirect('/apartment/')

def DialogAddApartment(request):
    formName='AddPodezd'
    if request.method == 'POST':
        print(request.POST.get('FormName'))
        if request.POST.get('FormName') == 'AddPodezd':

            PodezdForm = AddPodezd(request.POST)
            if PodezdForm.is_valid():
                podezd = Podezd()
                podezd.user = request.user
                podezd.numder =PodezdForm.cleaned_data['numder']
                podezd.note = PodezdForm.cleaned_data['note']
                podezd.save()
                formName = 'AddLevel'
                LevelForm1 = AddLevelForm(initial={'PodezdID': podezd.id})

                return render(request, "DialogAddApartment.html",
                              {'PodezdForm': PodezdForm, 'formName': formName,
                               'LevelForm': LevelForm1})

        elif request.POST.get('FormName') == 'AddLevel':
            lvl = AddLevelForm(request.POST)
            if lvl.is_valid():

                countlevel = lvl.cleaned_data['count_level']
                podezdID = lvl.cleaned_data['PodezdID']
                i = 1
                print('countlevel'+str(countlevel))
                while i <= countlevel:
                    print(i)
                    l = Level()
                    l.podezd_id = podezdID
                    l.level_number = i
                    l.save()
                    i += 1
                PodezdForm = AddPodezd()
                LevelForm = AddLevelForm()
                levelList=Level.objects.filter(podezd_id=podezdID).order_by('id').reverse()
                print(podezdID)
                formName = 'AddApartment'
                return render(request, "DialogAddApartment.html",
                                  {'PodezdForm': PodezdForm, 'formName': formName,
                                   'LevelForm': LevelForm, 'levelList':levelList})

        elif request.POST.get('FormName') == 'AddApartment':

            start_number = int(request.POST.get('StartNumber'))

            s =OrderedDict(sorted(request.POST.items()))
            for name,value in s.items():
                if 'Level' in name:
                    i=1
                    while i<=int(value):
                        a=Apartment()
                        a.level_id=name[5:]
                        a.numeber=start_number
                        a.save()
                        start_number+=1
                        i+=1
            return HttpResponseRedirect('/apartment/')
    PodezdForm=AddPodezd()
    LevelForm=AddLevelForm()
    return render(request, "DialogAddApartment.html",{'PodezdForm':PodezdForm,'formName':formName, 'LevelForm':LevelForm})

class editApartInfo(forms.Form):
    Apartment = forms.IntegerField(label='Apartment PK', widget = forms.HiddenInput())
    countRes = forms.IntegerField(label='Количество проживающих', widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))
    countRooms = forms.IntegerField(label='Количество комнат', widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))
    area = forms.IntegerField(label='Общая площадь', widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))
    HotArea = forms.IntegerField(label='Отопительная площадь', widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))
    isRent = forms.BooleanField(required=False)


def editApartament(request, pk):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        ea = editApartInfo(request.POST)
        # check whether it's valid:
        if ea.is_valid():
            a = Apartment.objects.get(id=pk)
            a.countResidents = ea.cleaned_data['countRes']
            a.countRooms = ea.cleaned_data['countRooms']
            a.area = ea.cleaned_data['area']
            a.HotArea = ea.cleaned_data['HotArea']
            a.isRent = ea.cleaned_data['isRent']
            a.subsidyi_id = request.POST.get('subs', '').strip()
            print(request.POST.get('subs', '').strip())
            a.save()
            return HttpResponseRedirect('/apartment/'+pk+'/edit/')

    addUserApartment = AddApartmentUser()


    owner = ''
    a = Apartment.objects.get(id=pk)
    ea = editApartInfo(
        {'Apartment': pk,
         'countRes': a.countResidents,
         'countRooms':a.countRooms,
         'area':a.area,
         'HotArea':a.HotArea,
         'isRent': a.isRent

         })

    ea.HotArea = a.HotArea
    if UserProfile.objects.filter(id = a.userprofile_id).exists():
        owner = UserProfile.objects.get(id = a.userprofile_id)
    CurTarrif = Tariffs.objects.filter(residents=pk)
    tariff= Tariffs.objects.filter(user=request.user)
    subs = subsidyi.objects.all()
    return render(request, "addApartment.html", {'pk':pk,'addUserApartment':addUserApartment,'owner':owner,'tariff':tariff,'CurTarrif':CurTarrif, 'Apart':a,'ea':ea, 'subs':subs})

def enableTarif(request):
    pk = request.GET.get('pk')
    idTarrif = request.GET.get('idTarrif')
    if request.GET.get('enable') == 'true':
        enable=True
        a = Apartment.objects.get(id=pk)
        t = Tariffs.objects.get(id=idTarrif)
        t.residents.remove(a)

        t.residents.add(a)


    else:
        enable=False
        print(pk)
        print(idTarrif)
        a = Apartment.objects.get(id=pk)
        t = Tariffs.objects.get(id=idTarrif)
        t.residents.remove(a)

    print(enable)
    return HttpResponse(pk, content_type='text/html')


class AddApartmentUser(forms.Form):
    FirstName = forms.CharField(label='Имя', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    LastName =forms.CharField(label='Фамилия', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(label='Отчество', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number = forms.CharField(label='Номер телефона', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    countRes = forms.IntegerField(label='Количество проживающих', widget=forms.TextInput(attrs={'class': 'form-control','type':'number'}))

def ApartamentAddUser(request):
    if request.method == 'POST':
        addUserApartment = AddApartmentUser(request.POST)
        if addUserApartment.is_valid():
            if UserProfile.objects.filter(number=addUserApartment.cleaned_data['number']):
                a = Apartment.objects.get(id =request.POST.get('apartID'))
                a.user = UserProfile.objects.get(number=addUserApartment.cleaned_data['number'])
                a.countResidents = addUserApartment.cleaned_data['countRes']
                a.save()
                print(a.user)
            else:
                p= UserProfile()
                p.number =addUserApartment.cleaned_data['number']
                p.FirstName =addUserApartment.cleaned_data['FirstName']
                p.LastName =addUserApartment.cleaned_data['LastName']
                p.patronymic =addUserApartment.cleaned_data['patronymic']
                p.isOSMD=False
                p.save()
                a = Apartment.objects.get(id=request.POST.get('apartID'))
                a.countResidents = addUserApartment.cleaned_data['countRes']
                a.userprofile=p
                a.save()
    return HttpResponseRedirect('/apartment/'+request.POST.get('apartID')+'/edit/')