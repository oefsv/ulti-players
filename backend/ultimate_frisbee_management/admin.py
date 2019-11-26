from django.contrib import admin
from . import models
# Register your models here.

class PersonAdmin(admin.ModelAdmin):
    list_display = ('id','firstname', 'lastname', 'birthdate','sex', 'user','eligibile_u17')
    list_display_links = ('id',)


admin.site.register(models.Person, PersonAdmin)
admin.site.register(models.Association)
admin.site.register(models.Club)
admin.site.register(models.Team)

