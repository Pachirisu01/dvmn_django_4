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

    entities = PokemonEntity.objects.select_related('pokemon').filter(
        appeared_at__lte=now,
        disappeared_at__gte=now
    )

    for entity in entities:
        pokemon = entity.pokemon
        if not pokemon:
            continue

        if pokemon.image and hasattr(pokemon.image, 'url'):
            image_url = request.build_absolute_uri(pokemon.image.url)
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
        if pokemon.image and hasattr(pokemon.image, 'url'):
            img_url = request.build_absolute_uri(pokemon.image.url)
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

    def get_pokemon_image_url(pokemon):
        if pokemon.image and hasattr(pokemon.image, 'url'):
            return request.build_absolute_uri(pokemon.image.url)
        return DEFAULT_IMAGE_URL


    marker_image_url = get_pokemon_image_url(pokemon)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for entity in pokemon.entities.all():
        add_pokemon(folium_map, entity.latitude, entity.longitude, marker_image_url)

    pokemon_data = {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en or '',
        'title_jp': pokemon.title_jp or '',
        'description': pokemon.description or '',
        'img_url': get_pokemon_image_url(pokemon),
    }

    if pokemon.evolution_from:
        prev = pokemon.evolution_from
        pokemon_data['previous_evolution'] = {
            'title_ru': prev.title,
            'pokemon_id': prev.pk,
            'img_url': get_pokemon_image_url(prev),
            'url': prev.get_absolute_url(),
        }

    next_pokemon = pokemon.next_evolutions.first()
    if next_pokemon:
        pokemon_data['next_evolution'] = {
            'title_ru': next_pokemon.title,
            'pokemon_id': next_pokemon.pk,
            'img_url': get_pokemon_image_url(next_pokemon),
            'url': next_pokemon.get_absolute_url(),
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data,
    })