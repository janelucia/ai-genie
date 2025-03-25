from django.contrib import admin
from .models import *

class ResearchModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    
# Register your models here.
admin.site.register(Event)
admin.site.register(Research, ResearchModelAdmin)
admin.site.register(Researcher)