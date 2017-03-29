from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from tariff.views import sumFormula
from tariff.models import *
from django.utils import timezone
# Create your views here.


def UserTariff(request,year,month):
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
        psum = request.POST.get('psum')

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
            u1.current_raadings = current
        elif tarType == 6:
            u1.current_raadings = psum
        elif tarType == 7:
            pass
        elif tarType ==8:
            u1.previous_readings = previous
            u1.current_raadings = current
        elif tarType ==9:
            u1.previous_readings = previous
            u1.current_raadings = current
            u1.previous_readings_c2 = previous_c2
            u1.current_raadings_c2 = current_c2
        elif tarType ==10:
            u1.previous_readings = previous
            u1.current_raadings = current
            u1.previous_readings_c2 = previous_c2
            u1.current_raadings_c2 = current_c2
        elif tarType ==11:
            u1.previous_readings = previous
            u1.current_raadings = current
            u1.previous_readings_c2 = previous_c2
            u1.current_raadings_c2 = current_c2
        # elif tarType ==12:
        #     u1.previous_readings = previous
        #     u1.current_raadings = current
        #     u1.previous_readings_c2 = previous_c2
        #     u1.current_raadings_c2 = current_c2
        # elif tarType ==13:
        #     u1.previous_readings = previous
        #     u1.current_raadings = current
        #     u1.previous_readings_c2 = previous_c2
        #     u1.current_raadings_c2 = current_c2
        u1.save()
        return HttpResponseRedirect('/UserTariff/00-0000/')

    if (year=='0000' and month == '00'):
        return HttpResponseRedirect('/UserTariff/'+str(timezone.now().month)+'-'+str(timezone.now().year)+'/')
    tar = []

    for t in  Tariffs.objects.filter(residents__userprofile__user=request.user):

        t.dat()
        t.apart = []
        tar.append(t)

        for ap in t.residents.filter( userprofile__user=request.user):
            ap.ut = []
            for util in Utilities.objects.filter(dateAdd__year= year, dateAdd__month=month,  apartment = ap , tarif = t):
                sumFormula(t, util)
                ap.ut.append(util)
            t.apart.append(ap)

    return render(request, "UserTariff.html",{'month':month,'year':year,'tar':tar})