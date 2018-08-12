from django.contrib import admin
from player_management import models
# Register your models here.

admin.site.register(models.Person)
admin.site.register(models.Player)
admin.site.register(models.Association)
admin.site.register(models.Club)
admin.site.register(models.Team)

