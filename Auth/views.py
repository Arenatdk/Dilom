from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from Auth.models import *
from django import forms
from django.contrib.auth.models import User

# Create your views here.
def login(request):
    if request.user.is_authenticated():
        if request.user.userprofile is None:
            return HttpResponseRedirect('/UserPanel/')
        if request.user.userprofile.isOSMD:
            return HttpResponseRedirect('/account/')
        else:
            return HttpResponseRedirect('/UserPanel/')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Правильный пароль и пользователь "активен"
            auth.login(request, user)
            if request.user.userprofile.isOSMD:
                return HttpResponseRedirect('/account/')
            else:
                return HttpResponseRedirect('/UserPanel/')
            # Перенаправление на "правильную" страницу

    return render(request, "login.html")


class UserOSMDForm(forms.Form):
    username = forms.CharField(max_length=30, label="",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    email = forms.CharField(max_length=30, label="",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email','type':'email'}))
    pass1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                            label="Пароль", min_length=6, max_length=30)
    pass2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль еще раз'}),
        label="Пароль ещё раз")
    FirstName = forms.CharField(max_length=30, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    LastName = forms.CharField(max_length=30, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))
    patronymic = forms.CharField(max_length=30, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'}))
    number = forms.CharField(max_length=20, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}))
    #TYPE=
    OSBBname = forms.CharField( required=False, max_length=50, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название организации'}))
    addres = forms.CharField( required=False, max_length=50, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город'}))
    street = forms.CharField( required=False, max_length=50, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Улица'}))
    homenumber = forms.CharField( required=False, max_length=10, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер'}))

    def clean_pass2(self):
        if (self.cleaned_data["pass2"] != self.cleaned_data.get("pass1", "")):
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data["pass2"]






def register(request):
    errors = {}
    if request.method == 'POST':

        form = UserOSMDForm(request.POST)
        if form.is_valid() and not User.objects.filter(username=form.cleaned_data['username']).exists():
            t=User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['pass1'])
            t.userprofile.FirstName = form.cleaned_data['FirstName']
            t.userprofile.LastName = form.cleaned_data['LastName']
            t.userprofile.patronymic = form.cleaned_data['patronymic']
            t.userprofile.number = form.cleaned_data['number']

            print(request.POST)
            print(request.POST.get('myCheckBox'))
            if 'myCheckBox' in request.POST:

                print('daaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                t.userprofile.isOSMD=True
                t.userprofile.OSBBname = form.cleaned_data['OSBBname']
                t.userprofile.addres = form.cleaned_data['addres']
                t.userprofile.street = form.cleaned_data['street']
                t.userprofile.homenumber = form.cleaned_data['homenumber']
            else:
                t.userprofile.isOSMD=False
                print('neeeeeeeee')
            t.userprofile.save()
            user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['pass1'])






            auth.login(request, user)
            if t.userprofile.isOSMD:
                return HttpResponseRedirect('/account/')
            else:
                return HttpResponseRedirect('/UserPanel/')
        else:
            errors['username'] ='Логин занят'
    else:
        #errors['username'] = 'sdsfdfsdfsdf'
        form = UserOSMDForm()
        # tariff_type = Tariff_type.objects.all()
    return render(request, "register.html", {'form': form,'errors': errors})




def logout(request):
    auth.logout(request)
    # Перенаправление на страницу.
    return HttpResponseRedirect("/")
#---------------

