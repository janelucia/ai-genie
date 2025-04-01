from django.contrib import admin
from .models import *

class ResearchModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class MessageModelAdmin(admin.ModelAdmin):
    list_filter = ["chat__id"]

# Register your models here.
admin.site.register(Event)
admin.site.register(Research, ResearchModelAdmin)
admin.site.register(Researcher)
admin.site.register(Chat)
admin.site.register(Message, MessageModelAdmin)