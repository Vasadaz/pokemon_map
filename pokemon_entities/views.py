import folium

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import Pokemon, PokemonEntity


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


def get_pokemon_notes(request, pokemon_objects) -> dict:
    pokemon_img_url = request.build_absolute_uri('/media/' + str(pokemon_objects.image))

    pokemon = {
        'pokemon_id': pokemon_objects.id,
        'title_ru': pokemon_objects.title,
        'title_en': pokemon_objects.title_en,
        'title_jp': pokemon_objects.title_jp,
        'description': pokemon_objects.description,
        'img_url': pokemon_img_url,
    }

    return pokemon


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now_at = localtime().now()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__date__lt=now_at,
        disappeared_at__date__gt=now_at,
    ).values('lat', 'long')

    for pokemon in pokemons:
        pokemon_notes = get_pokemon_notes(request, pokemon)
        pokemons_on_page.append(pokemon_notes)

        for pokemon_entity in pokemon_entities.filter(pokemon=pokemon):
            add_pokemon(
                folium_map,
                pokemon_entity['lat'],
                pokemon_entity['long'],
                pokemon_notes['img_url'],
            )

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon_notes = get_pokemon_notes(request, pokemon)
    now_at = localtime().now()
    pokemon_entities = PokemonEntity.objects.filter(
        pokemon=pokemon,
        appeared_at__date__lt=now_at,
        disappeared_at__date__gt=now_at,
    ).values('lat', 'long')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map,
            pokemon_entity['lat'],
            pokemon_entity['long'],
            pokemon_notes['img_url'],
        )
    if pokemon.next_evolution:
        pokemon_notes['next_evolution'] = get_pokemon_notes(request, pokemon.next_evolution)

    try:
        parent_pokemon = pokemon.previous_evolutions.get()
        pokemon_notes['previous_evolution'] = get_pokemon_notes(request, parent_pokemon)
    except Pokemon.DoesNotExist:
        pokemon_notes['previous_evolution'] = None

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_notes
    })
