from django.shortcuts import render
from apartments.models import Apartment

# Create your views here.
def panel(request):
    a = Apartment.objects.get(userprofile__user=request.user)
    return render(request, "UserPanel.html",{'Apart':a})