import folium
from django.utils.timezone import localtime
from django.shortcuts import get_object_or_404

from django.shortcuts import render
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


def show_all_pokemons(request):

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    now = localtime()

    entities = PokemonEntity.objects.select_related('subject').filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )

    for entity in entities:
        pokemon = entity.subject
        if not pokemon:
            continue

        if pokemon.pokemon_image and hasattr(pokemon.pokemon_image, 'url'):
            image_url = request.build_absolute_uri(pokemon.pokemon_image.url)
        elif pokemon.img_url:
            image_url = pokemon.img_url
        else:
            image_url = DEFAULT_IMAGE_URL

        add_pokemon(
            folium_map,
            entity.latitude,
            entity.longitude,
             image_url,
        )

    pokemons_on_page = []
    all_pokemons = Pokemon.objects.all()

    for pokemon in all_pokemons:
        if pokemon.pokemon_image and hasattr(pokemon.pokemon_image, 'url'):
            img_url = request.build_absolute_uri(pokemon.pokemon_image.url)
        elif pokemon.img_url:
            img_url = pokemon.img_url
        else:
            img_url = DEFAULT_IMAGE_URL
        pokemon_info = {
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        }
        pokemons_on_page.append(pokemon_info)

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):

    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    entities = PokemonEntity.objects.filter(subject=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in entities:
        if pokemon.pokemon_image and hasattr(pokemon.pokemon_image, 'url'):
            image_url = request.build_absolute_uri(pokemon.pokemon_image.url)
        elif pokemon.img_url:
            image_url = pokemon.img_url
        else:
            image_url = DEFAULT_IMAGE_URL

        add_pokemon(folium_map, entity.latitude, entity.longitude, image_url)

    img_final = (
        request.build_absolute_uri(pokemon.pokemon_image.url)
        if pokemon.pokemon_image and hasattr(pokemon.pokemon_image, 'url')
        else (pokemon.img_url or DEFAULT_IMAGE_URL)
    )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'img_url': img_final,
        'description': pokemon.description,
    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data,
    })