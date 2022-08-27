from django.contrib import admin

from .models import Pokemon


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

admin.site.register(Pokemon, PokemonAdmin)