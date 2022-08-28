import os.path

import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_img_url = request.build_absolute_uri('/media/' + str(pokemon.image))
        for pokemon_entity in pokemon.entities.values():
            now_at = localtime().now().timetuple()
            appeared_at = pokemon_entity['appeared_at'].timetuple()
            disappeared_at = pokemon_entity['disappeared_at'].timetuple()

            if appeared_at < now_at < disappeared_at:
                add_pokemon(
                    folium_map,
                    pokemon_entity['lat'],
                    pokemon_entity['long'],
                    pokemon_img_url,
                )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': os.path.join('media', str(pokemon.image)),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon_objects = Pokemon.objects.get(id=pokemon_id)
        pokemon_img_url = request.build_absolute_uri('/media/' + str(pokemon_objects.image))
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_objects.entities.values():
        now_at = localtime().now().timetuple()
        appeared_at = pokemon_entity['appeared_at'].timetuple()
        disappeared_at = pokemon_entity['disappeared_at'].timetuple()

        if appeared_at < now_at < disappeared_at:
            add_pokemon(
                folium_map,
                pokemon_entity['lat'],
                pokemon_entity['long'],
                pokemon_img_url,
            )

    pokemon = {
        'title_ru': pokemon_objects.title,
        'title_en': pokemon_objects.title_en,
        'title_jp': pokemon_objects.title_jp,
        'description': pokemon_objects.description,
        'img_url': pokemon_img_url,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
