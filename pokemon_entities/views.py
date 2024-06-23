import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon, PokemonEntity

from django.utils.timezone import localtime, activate


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
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    activate('Europe/Moscow')
    current_time = localtime()

    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lt=current_time,
                                                       disappeared_at__gt=current_time):
        pokemon = pokemon_entity.pokemon
        img_url = request.build_absolute_uri(pokemon.image.url)
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'title': pokemon.title,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        "title_jp": pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url)
        }
    }


    activate('Europe/Moscow')
    current_time = localtime()
    img_url = request.build_absolute_uri(pokemon.image.url)

    if PokemonEntity.objects.filter(pokemon=pokemon.id, appeared_at__lt=current_time, disappeared_at__gt=current_time):
        folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
        for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon,
                                                           appeared_at__lt=current_time,
                                                           disappeared_at__gt=current_time):
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                img_url
            )
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')


    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page
    })


