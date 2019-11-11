from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.Association)
admin.site.register(models.Club)
admin.site.register(models.Team)

