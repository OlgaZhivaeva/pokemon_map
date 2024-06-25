import folium

from django.shortcuts import render, get_object_or_404

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
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    previous_evolution = {}
    previous = pokemon.previous_evolution
    if previous:
        previous_evolution = {
            'pokemon_id': previous.id,
            'title_ru': previous.title,
            'img_url': request.build_absolute_uri(previous.image.url)
        }

    next_evolution = {}
    next = pokemon.next_evolutions.first()
    if next:
        next_evolution = {
            'pokemon_id': next.id,
            'title_ru': next.title,
            'img_url': request.build_absolute_uri(next.image.url)
        }

    pokemon_on_page = {
        'pokemon_id': pokemon.id,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'title': pokemon.title,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        "title_jp": pokemon.title_jp,
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    activate('Europe/Moscow')
    current_time = localtime()
    img_url = request.build_absolute_uri(pokemon.image.url)

    active_pokemon_еntities = PokemonEntity.objects.filter(pokemon=pokemon.id,
                                                           appeared_at__lt=current_time,
                                                           disappeared_at__gt=current_time)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in active_pokemon_еntities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_on_page
    })
