from django.db import models
from django.urls import reverse

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название Покемона',
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Английское название',
        blank=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Японское название',
        blank=True,
    )
    image = models.ImageField(
        upload_to='pokemon_image',
        verbose_name='Картинка',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    evolution_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_evolutions',
        verbose_name='Из кого эволюционировал'
    )

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('pokemon', args=[self.id])

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        null=True,
        blank=True,
        verbose_name='Покемон',
        related_name='entities',
        on_delete=models.CASCADE
    )
    longitude = models.FloatField(
        verbose_name='Долгота',
    )
    latitude = models.FloatField(
        verbose_name='Широта',
    )
    appeared_at = models.DateTimeField(
        verbose_name='Появится',
        null=True,
        blank=True
    )
    disappeared_at = models.DateTimeField(
        verbose_name='Исчезнет',
        null=True,
        blank=True
    )
    level = models.IntegerField(
        verbose_name='Уровень',
        null=True,
        blank=True
    )
    health = models.IntegerField(
        verbose_name='Здоровье',
        null=True,
        blank=True
    )
    strength = models.IntegerField(
        verbose_name='Сила',
        null=True,
        blank=True
    )
    defence = models.IntegerField(
        verbose_name='Защита',
        null=True,
        blank=True
    )
    stamina = models.IntegerField(
        verbose_name='Выносливость',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.pokemon.title} ({self.latitude:.4f}, {self.longitude:.4f})'