from django.db import models

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Pokemon name',
    )
    pokemon_image = models.ImageField(
        upload_to='media',
        verbose_name='Images',
        null=True,
        blank=True,
    )
    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    longitude = models.FloatField(verbose_name='Lon')
    latitude = models.FloatField(verbose_name='Lat')
    def __str__(self):
        return f'{self.name} ({self.latitude:.4f}, {self.longitude:.4f})'