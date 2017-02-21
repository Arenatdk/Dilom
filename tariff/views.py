
from django import forms
from django.shortcuts import render
from tariff.models import *
from django.http import HttpResponseRedirect
from apartments.models import Apartment
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse



class add_tariffForm(forms.Form):
    name = forms.CharField(max_length=100,label="", widget = forms.TextInput(attrs={'class': 'form-control'}))
    fariff_type = forms.ModelChoiceField(queryset=Tariff_type.objects.all(), initial=0, widget=forms.Select(attrs={'class':'form-control', 'onchange' : 'filter()'}))
    price = forms.CharField(required=False,max_length=15,label="Еденица измерения", widget = forms.TextInput(attrs={'class': 'form-control'}))
    pricefor1 = forms.FloatField( required=False,min_value=0,label="Цена за единицу", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    pricefor1CB = forms.BooleanField( required=False,)
    comment= forms.CharField( required=False,max_length=100,label="Комментарий", widget = forms.TextInput(attrs={'class': 'form-control'}))
    porog1 = forms.FloatField( required=False,min_value=0,label="1 порог", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    pricefor2 = forms.FloatField( required=False,min_value=0,label="Цена за единицу", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    pricefor2CB = forms.BooleanField( required=False)
    porog2 = forms.FloatField( required=False,min_value=0,label="2 порог", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    pricefor3 = forms.FloatField( required=False,min_value=0,label="Цена за единицу", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    pricefor3CB = forms.BooleanField( required=False)
    sum = forms.FloatField( required=False,min_value=0,label="Сумма", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    T1price = forms.FloatField( required=False,min_value=0,label="Т1, Цена за 1 единицу", widget = forms.TextInput(attrs={'class': 'form-control','type':'number','step':'any'}))
    T1priceCB = forms.BooleanField(required=False)
    T2price = forms.FloatField(required=False, min_value=0, label="Т1, Цена за 1 единицу", widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T2priceCB = forms.BooleanField(required=False)
    T1price1 = forms.FloatField(required=False, min_value=0, label="Т1, Цена за 1 единицу",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T1priceCB1 = forms.BooleanField(required=False)
    T2price1 = forms.FloatField(required=False, min_value=0, label="Т1, Цена за 1 единицу",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T2priceCB1 = forms.BooleanField(required=False)
    T1price2 = forms.FloatField(required=False, min_value=0, label="Т1, Цена за 1 единицу",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T1priceCB2 = forms.BooleanField(required=False)
    T2price2 = forms.FloatField(required=False, min_value=0, label="Т1, Цена за 1 единицу",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T2priceCB2 = forms.BooleanField(required=False)
    T1Porog = forms.FloatField(required=False, min_value=0, label="T1, 1 порог",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T2Porog = forms.FloatField(required=False, min_value=0, label="T2, 1 порог",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T1Porog1 = forms.FloatField(required=False, min_value=0, label="T1, 2 порог",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    T2Porog1 = forms.FloatField(required=False, min_value=0, label="T2, 2 порог",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    ObshPorog = forms.FloatField(required=False, min_value=0, label="Общий порог",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))
    ObshPorog1 = forms.FloatField(required=False, min_value=0, label="Общий порог 2",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number','step':'any'}))



def index_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    return render(request,"index.html")



def tarif_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    tarif_list=Tariffs.objects.filter(user=request.user)

    return render(request,"tariffs.html",{'tarif_list':tarif_list})

from django.http import JsonResponse
def pattern_ajax(request):
    PatID = int(request.GET.get('patID'))
    if PatID == 0:
        return  HttpResponse('')
    ptrn = Patterns.objects.get(id=PatID)

    return HttpResponse('{ "name" : "'+ptrn.unit_measure+'", "id" : "' + str(ptrn.type_id) + '"}')


def add_taritt(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':

        form = add_tariffForm(request.POST)

        if form.is_valid():
            id_type = int(request.POST.get('fariff_type', '').strip())
            t = Tariffs()
            t.name = form.cleaned_data['name']
            t.coment = form.cleaned_data['comment']
            t.user = request.user
            if id_type==1:
                t.unit_measure =  form.cleaned_data['price']
                t.type_id = 1
                t.enable = True
                t.price0_t1 = form.cleaned_data['pricefor1']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
            elif id_type==2:
                t.unit_measure = form.cleaned_data['price']
                t.type_id = 2
                t.enable = True
                t.price0_t1 = form.cleaned_data['pricefor1']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
                t.level1_t1 = form.cleaned_data['porog1']
                t.price1_t1 = form.cleaned_data['pricefor2']
                t.benefit1_t1 = form.cleaned_data['pricefor2CB']
            elif id_type==3:
                t.unit_measure = form.cleaned_data['price']
                t.type_id = 3
                t.enable = True
                t.price0_t1 = form.cleaned_data['pricefor1']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
                t.level1_t1 = form.cleaned_data['porog1']
                t.price1_t1 = form.cleaned_data['pricefor2']
                t.benefit1_t1 = form.cleaned_data['pricefor2CB']
                t.level2_t1 = form.cleaned_data['porog2']
                t.price2_t1 = form.cleaned_data['pricefor3']
                t.benefit2_t1 = form.cleaned_data['pricefor3CB']
            elif id_type==4:
                t.unit_measure =  form.cleaned_data['price']
                t.type_id = 4
                t.enable = True
                t.price0_t1 = form.cleaned_data['pricefor1']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
            elif id_type == 5:
                t.unit_measure = form.cleaned_data['price']
                t.type_id = 5
                t.enable = True
                t.price0_t1 = form.cleaned_data['pricefor1']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
            elif id_type == 6:
                t.type_id = 6
                t.enable = True
            elif id_type==7:
                t.type_id = 7
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
            elif id_type == 8:
                t.unit_measure = form.cleaned_data['price']
                t.type_id = 8
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']
            elif id_type==9:
                t.type_id = 9
                t.price0_t1 = form.cleaned_data['T1price']
                t.benefit0_t1 = form.cleaned_data['T1priceCB']
                t.price0_t2 = form.cleaned_data['T2price']
                t.benefit0_t2 = form.cleaned_data['T2priceCB']
                t.unit_measure = form.cleaned_data['price']
                t.enable = True
            elif id_type==10:
                t.type_id = 10
                t.price0_t1 = form.cleaned_data['T1price']
                t.benefit0_t1 = form.cleaned_data['T1priceCB']
                t.price0_t2 = form.cleaned_data['T2price']
                t.benefit0_t2 = form.cleaned_data['T2priceCB']
                t.level1_t1=  form.cleaned_data['T1Porog']
                t.level1_t2=  form.cleaned_data['T2Porog']
                t.price1_t1 = form.cleaned_data['T1price1']
                t.benefit1_t1 = form.cleaned_data['T1priceCB1']
                t.price1_t2 = form.cleaned_data['T2price1']
                t.benefit1_t2 = form.cleaned_data['T2priceCB1']
                t.unit_measure = form.cleaned_data['price']
                t.enable = True
            elif id_type==11:
                t.type_id = 11
                t.price0_t1 = form.cleaned_data['T1price']
                t.benefit0_t1 = form.cleaned_data['T1priceCB']
                t.price0_t2 = form.cleaned_data['T2price']
                t.benefit0_t2 = form.cleaned_data['T2priceCB']


                t.level1_t1 = form.cleaned_data['T1Porog']
                t.level1_t2 = form.cleaned_data['T2Porog']


                t.price1_t1 = form.cleaned_data['T1price1']
                t.benefit1_t1 = form.cleaned_data['T1priceCB1']
                t.price1_t2 = form.cleaned_data['T2price1']
                t.benefit1_t2 = form.cleaned_data['T2priceCB1']

                t.level2_t1 = form.cleaned_data['T1Porog1']
                t.level2_t2 = form.cleaned_data['T2Porog1']

                t.price2_t1 = form.cleaned_data['T1price2']
                t.benefit2_t1 = form.cleaned_data['T1priceCB2']
                t.price2_t2 = form.cleaned_data['T2price2']
                t.benefit2_t2 = form.cleaned_data['T2priceCB2']
                t.unit_measure = form.cleaned_data['price']
                t.enable = True

            elif id_type == 12:
                t.type_id = 12
                t.price0_t1 = form.cleaned_data['T1price']
                t.benefit0_t1 = form.cleaned_data['T1priceCB']
                t.price0_t2 = form.cleaned_data['T2price']
                t.benefit0_t2 = form.cleaned_data['T2priceCB']

                t.level1_t1 = form.cleaned_data['ObshPorog']

                t.price1_t1 = form.cleaned_data['T1price1']
                t.benefit1_t1 = form.cleaned_data['T1priceCB1']
                t.price1_t2 = form.cleaned_data['T2price1']
                t.benefit1_t2 = form.cleaned_data['T2priceCB1']
                t.unit_measure = form.cleaned_data['price']
                t.enable = True
            elif id_type == 13:
                t.type_id = 13
                t.price0_t1 = form.cleaned_data['T1price']
                t.benefit0_t1 = form.cleaned_data['T1priceCB']
                t.price0_t2 = form.cleaned_data['T2price']
                t.benefit0_t2 = form.cleaned_data['T2priceCB']

                t.level1_t1 = form.cleaned_data['ObshPorog']


                t.price1_t1 = form.cleaned_data['T1price1']
                t.benefit1_t1 = form.cleaned_data['T1priceCB1']
                t.price1_t2 = form.cleaned_data['T2price1']
                t.benefit1_t2 = form.cleaned_data['T2priceCB1']

                t.level2_t1 = form.cleaned_data['ObshPorog1']


                t.price2_t1 = form.cleaned_data['T1price2']
                t.benefit2_t1 = form.cleaned_data['T1priceCB2']
                t.price2_t2 = form.cleaned_data['T2price2']
                t.benefit2_t2 = form.cleaned_data['T2priceCB2']
                t.unit_measure = form.cleaned_data['price']
                t.enable = True
            elif id_type == 14:
                t.type_id = 14
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']

            elif id_type == 15:
                t.type_id = 15
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']

            elif id_type == 16:
                t.type_id = 16
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']

            elif id_type == 17:
                t.type_id = 17
                t.enable = True
                t.price0_t1 = form.cleaned_data['sum']
                t.benefit0_t1 = form.cleaned_data['pricefor1CB']

            t.save()
            for a in Apartment.objects.filter(level__podezd__user=request.user).order_by('id'):
                t.residents.add(a) # Тест для добавления обной квартиры
           # t.residents.add(Apartment.objects.filter(id=16514))
            return HttpResponseRedirect('/tariff/')


    else:
        form = add_tariffForm()
    tariff_type = Tariff_type.objects.all()
    patrn = Patterns.objects.all()
    return render(request,"add_tariff.html",{'tariff_type':tariff_type,'form': form,'patrn':patrn})




def contribution(request,year,month):
    if request.is_ajax():
        print(request)
        apID = request.GET.get('apID')
        tarID = request.GET.get('tarID')
        u =Utilities.objects.filter(apartment_id=apID, tarif_id=tarID).order_by('dateAdd').last()
        if u:
            v = '{"priv1": '+str(u.current_raadings)+' , "priv2": '+str(u.current_raadings_c2)+' }'
            return HttpResponse(v, content_type='text/html')
        else:
            return HttpResponse('none', content_type='text/html')
    if request.method == 'POST':
        tarID = request.POST.get('tarID')
        apID = request.POST.get('apID')
        tarType = int(request.POST.get('tarType'))
        dateAdd = request.POST.get('datap')

        previous = request.POST.get('previous')
        current = request.POST.get('current')
        previous_c2 = request.POST.get('previous_c2')
        current_c2 = request.POST.get('current_c2')

        #print(tarID)
        #print(apID)
        #print(dateAdd)
        print(tarType)
        print(previous)
        print(current)
        u1 = Utilities()
        u1.tarif_id = tarID
        u1.apartment_id = apID
        u1.dateAdd = dateAdd
        if tarType == 1:
            u1.previous_readings = previous
            u1.current_raadings = current
        elif tarType == 2:
            u1.previous_readings = previous
            u1.current_raadings = current
        elif tarType == 3:
            u1.previous_readings = previous
            u1.current_raadings = current
        elif tarType == 4:
            u1.previous_readings = previous
            u1.current_raadings = current
            u1.previous_readings_c2 = previous_c2
            u1.current_raadings_c2 = current_c2
        elif tarType == 5:
            u1.current_raadings = previous
        elif tarType == 6:
            u1.current_raadings = previous
        elif tarType == 7:
            pass
        u1.save()
        return HttpResponseRedirect('/contribution/00-0000/')

    if (year=='0000' and month == '00'):
        return HttpResponseRedirect('/contribution/'+str(timezone.now().month)+'-'+str(timezone.now().year)+'/')
    tar = []

    for t in  Tariffs.objects.filter(user=request.user):
        t.apart = []
        tar.append(t)

        for ap in t.residents.all():
            ap.ut = []
            for util in Utilities.objects.filter(dateAdd__year= year, dateAdd__month=month,  apartment = ap , tarif = t):
                if t.type_id == 1:
                    util.cur = util.current_raadings - util.previous_readings
                    if t.benefit0_t1 and util.apartment.subsidyi:
                        util.sum = round( ((util.current_raadings - util.previous_readings) * t.price0_t1 ) - (((util.current_raadings - util.previous_readings) * t.price0_t1 )*util.apartment.subsidyi.percent/100) , 2)
                        util.formula = str(util.current_raadings - util.previous_readings) + '*' + str(t.price0_t1) +'-' + str(util.apartment.subsidyi.percent )+ '%'
                        # Со льготами
                    else:
                        util.sum = round((util.current_raadings - util.previous_readings)*t.price0_t1, 2)
                        util.formula = str(util.current_raadings - util.previous_readings) + '*' + str(t.price0_t1)
                        # Без льгот
                elif t.type_id == 2:
                    util.cur = util.current_raadings - util.previous_readings
                    if t.benefit0_t1 and util.apartment.subsidyi :
                        util.sum = round((util.current_raadings - util.previous_readings) * t.price0_t1 - ((util.current_raadings - util.previous_readings) * t.price0_t1)*util.apartment.subsidyi.percent/100, 2)
                        util.formula = str(util.current_raadings - util.previous_readings) + '*' + str(t.price0_t1) + '-' + str(util.apartment.subsidyi.percent) + '%'
                        #Со льготами
                    else:
                        util.sum = round((util.current_raadings - util.previous_readings) * t.price0_t1, 2)
                        util.formula = str(util.current_raadings - util.previous_readings) + '*' + str(t.price0_t1)
                        #Без льгот
                    if (util.current_raadings - util.previous_readings) > t.level1_t1: # Первый порог
                        if t.benefit1_t1 and util.apartment.subsidyi:
                            util.sum = util.sum + round((util.current_raadings - util.previous_readings - t.level1_t1 ) * t.price1_t1 - ((util.current_raadings - util.previous_readings - t.level1_t1 ) * t.price1_t1*util.apartment.subsidyi.percent /100), 2)
                            util.formula = util.formula+'+' + str(util.current_raadings - util.previous_readings - t.level1_t1)+ '*'+ str(t.price1_t1)+'-'+ str(util.apartment.subsidyi.percent)+'%'
                            # Со льготами первый порог
                        else:
                            util.sum = util.sum + round((util.current_raadings - util.previous_readings - t.level1_t1) * t.price1_t1 ,2)
                            util.formula = util.formula +'+'+ str(util.current_raadings - util.previous_readings - t.level1_t1) + '*' + str(t.price1_t1)
                            # Без льгот первый порог







                elif t.type_id == 3:
                    util.cur = util.current_raadings - util.previous_readings
                    if util.cur <= t.level1_t1 : # Первый порог
                        if t.benefit0_t1 and util.apartment.subsidyi:
                            util.sum = round((util.cur * t.price0_t1) - (util.cur * t.price0_t1)* util.apartment.subsidyi.percent/100 , 2)
                            util.formula = str(util.cur) + '*' + str(t.price0_t1) + '-'+ str(util.apartment.subsidyi.percent)+ '%'
                        else:
                            util.sum =  round(util.cur * t.price0_t1 ,2)
                            util.formula =  str(util.cur)+'*'+ str(t.price0_t1)

                    if util.cur > t.level1_t1 and util.cur <= t.level2_t1 : # Первый порог
                        if t.benefit0_t1 and util.apartment.subsidyi:
                            util.sum = round((t.level1_t1 * t.price0_t1) - (t.level1_t1 * t.price0_t1)* util.apartment.subsidyi.percent/100 , 2)
                            util.formula = str(t.level1_t1) + '*' + str(t.price0_t1) + '-'+ str(util.apartment.subsidyi.percent)+ '%'
                        else:
                            util.sum =  round(t.level1_t1 * t.price0_t1 ,2)
                            util.formula =  str(t.level1_t1)+'*'+ str(t.price0_t1)


                        if t.benefit1_t1 and util.apartment.subsidyi:
                            util.sum = util.sum + round((util.cur - t.level1_t1) * t.price1_t1  - ((util.cur - t.level1_t1) * t.price1_t1)* util.apartment.subsidyi.percent/100, 2)
                            util.formula = util.formula + '+' + str(util.cur - t.level1_t1) + '*' + str(t.price1_t1) + '-' + str(util.apartment.subsidyi.percent) + '%'
                        else:
                            util.sum = util.sum + round((util.cur-t.level1_t1)*t.price1_t1  , 2)
                            util.formula = util.formula+'+'+ str(util.cur-t.level1_t1) + '*' + str(t.price1_t1)

                    if util.cur > t.level2_t1: # Третий порог
                        if t.benefit0_t1 and util.apartment.subsidyi:
                            util.sum = round((t.level1_t1 * t.price0_t1) - (t.level1_t1 * t.price0_t1)* util.apartment.subsidyi.percent/100 , 2)
                            util.formula = str(t.level1_t1) + '*' + str(t.price0_t1) + '-'+ str(util.apartment.subsidyi.percent)+ '%'
                        else:
                            util.sum =  round(t.level1_t1 * t.price0_t1 ,2)
                            util.formula =  str(t.level1_t1)+'*'+ str(t.price0_t1)

                        if t.benefit1_t1 and util.apartment.subsidyi:
                            util.sum = util.sum + round((t.level2_t1 - t.level1_t1) * t.price1_t1  - ((t.level2_t1 - t.level1_t1) * t.price1_t1)* util.apartment.subsidyi.percent/100, 2)
                            util.formula = util.formula + '+' + str(t.level2_t1 - t.level1_t1) + '*' + str(t.price1_t1) + '-' + str(util.apartment.subsidyi.percent) + '%'
                        else:
                            util.sum = util.sum + round((t.level2_t1 - t.level1_t1)*t.price1_t1  , 2)
                            util.formula = util.formula+'+'+ str(t.level2_t1 - t.level1_t1) + '*' + str(t.price1_t1)

                        if t.benefit2_t1 and util.apartment.subsidyi:
                            util.sum = util.sum + round((util.cur - t.level2_t1) * t.price2_t1 - ((util.cur - t.level2_t1) * t.price2_t1) * util.apartment.subsidyi.percent / 100, 2)
                            util.formula = util.formula + '+' + str(util.cur - t.level2_t1 ) + '*' + str(t.price2_t1) + '-' + str(util.apartment.subsidyi.percent) + '%'
                        else:
                            util.sum = util.sum + round((util.cur - t.level2_t1) * t.price2_t1, 2)
                            util.formula = util.formula + '+' + str(util.cur - t.level2_t1) + '*' + str(t.price2_t1)




                elif t.type_id == 4:
                    util.cur = util.current_raadings - util.previous_readings
                    util.cur_c2 = util.current_raadings_c2 - util.previous_readings_c2
                    util.sum = round(((util.current_raadings - util.previous_readings) + (util.current_raadings_c2 - util.previous_readings_c2)) *t.price0_t1, 2)
                    util.formula ='('+ str(util.current_raadings - util.previous_readings) +' + '+str(util.current_raadings_c2 - util.previous_readings_c2) + ') *' + str(t.price0_t1)
                elif t.type_id == 5:
                    util.cur = util.current_raadings
                    util.sum = round( util.current_raadings * t.price0_t1, 2)
                    util.formula = str(util.current_raadings) +'*'+ str(t.price0_t1)
                elif t.type_id == 6:
                    util.cur = util.current_raadings
                    util.sum = util.current_raadings
                    util.formula = str(util.current_raadings)
                elif t.type_id == 7:
                    util.sum = t.price0_t1
                elif t.type_id == 14:
                    util.sum = ap.countResidents
                    util.formula = str(util.current_raadings)
                ap.ut.append(util)
            t.apart.append(ap)

    return render(request, "contribution.html",{'month':month,'year':year,'tar':tar})
