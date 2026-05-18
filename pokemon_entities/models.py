from django.db import models

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название Покемона',
    )
    title_en = models.CharField(
        max_length=200,
        verbose_name='Английское название',
        blank=True,
        null=True,
    )
    title_jp = models.CharField(
        max_length=200,
        verbose_name='Японское название',
        blank=True,
        null=True,
    )
    pokemon_image = models.ImageField(
        upload_to='pokemon_image',
        verbose_name='Картинка',
        null=True,
        blank=True,
    )
    id = models.BigAutoField(primary_key=True)
    img_url = models.URLField(
        verbose_name='URL картинки',
        null=True,
        blank=True)
    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True)
    evolution_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evolutions',
        verbose_name='Из кого эволюционировал')


    def __str__(self):
        return f'{self.title}'

class PokemonEntity(models.Model):
    subject = models.ForeignKey(
        Pokemon,
        null=True,
        verbose_name='Покемон',
        on_delete=models.CASCADE)
    longitude = models.FloatField(
        verbose_name='Долгота',
        null=True,
        blank=True)
    latitude = models.FloatField(
        verbose_name='Широта',
        null=True,
        blank=True)
    appeared_at = models.DateTimeField(
        verbose_name='Появится',
        null=True,
        blank=True)
    disappeared_at = models.DateTimeField(
        verbose_name='Исчезнет',
        null=True,
        blank=True)
    pokemon_lvl = models.IntegerField(
        verbose_name='Уровень',
        null=True,
        blank=True)
    pokemon_hlth = models.IntegerField(
        verbose_name='Здоровье',
        null=True,
        blank=True)
    pokemon_strength = models.IntegerField(
        verbose_name='Сила',
        null=True,
        blank=True)
    pokemon_def = models.IntegerField(
        verbose_name='Защита',
        null=True,
        blank=True)
    pokemon_stam = models.IntegerField(
        verbose_name='Выносливость',
        null=True,
        blank=True)
    def __str__(self):
        return f'{self.subject.title} ({self.latitude:.4f}, {self.longitude:.4f})'
