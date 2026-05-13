from django.db import models

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Pokemon name',
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='English name',
        blank=True,
        null=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Japanese name',
        blank=True,
        null=True,
    )
    pokemon_image = models.ImageField(
        upload_to='media',
        verbose_name='Images',
        null=True,
        blank=True,
    )
    id = models.BigAutoField(primary_key=True)
    img_url = models.URLField(null=True,blank=True)
    description = models.TextField(verbose_name='Description',null=True,blank=True)
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
    pokemon_lvl = models.IntegerField(verbose_name='Level', null=True)
    pokemon_hlth = models.IntegerField(verbose_name='Health', null=True)
    pokemon_strength = models.IntegerField(verbose_name='Strength', null=True)
    pokemon_def = models.IntegerField(verbose_name='Defence', null=True)
    pokemon_stam = models.IntegerField(verbose_name='Stamina', null=True)
    def __str__(self):
        return f'{self.subject.title} ({self.latitude:.4f}, {self.longitude:.4f})'