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
    subject = models.ForeignKey(
        Pokemon,
        null=True,
        verbose_name='Pokemon',
        on_delete=models.CASCADE)
    longitude = models.FloatField(verbose_name='Lon')
    latitude = models.FloatField(verbose_name='Lat')
    appeared_at = models.DateTimeField(verbose_name='Appeared at', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Disappeared at', null=True)
    def __str__(self):
        return f'{self.name} ({self.latitude:.4f}, {self.longitude:.4f})'