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