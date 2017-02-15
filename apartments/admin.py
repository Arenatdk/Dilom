from django.contrib import admin
from .models import Level
from .models import Podezd
from .models import Apartment

class PodezdAdmin(admin.ModelAdmin):
    list_display = ['user','numder']

class LevelAdmin(admin.ModelAdmin):
    list_display = ['podezd','level_number']

admin.site.register(Podezd,PodezdAdmin)
admin.site.register(Level)
admin.site.register(Apartment)


