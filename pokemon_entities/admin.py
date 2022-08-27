from django.contrib import admin

from .models import Pokemon, PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')


class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'lat', 'long', 'appeared_at', 'disappeared_at', 'level')


admin.site.register(Pokemon, PokemonAdmin)
admin.site.register(PokemonEntity, PokemonEntityAdmin)