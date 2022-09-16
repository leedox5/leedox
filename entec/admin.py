from django.contrib import admin

from entec.models import Game
from entec.models import Match

# Register your models here.
admin.site.register(Game)
admin.site.register(Match)

class MatchAdmin(admin.ModelAdmin):
    search_fields = ['desc']

admin.site.register(Match, MatchAdmin)
