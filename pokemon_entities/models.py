from django.db import models

class Pokemon(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Pokemon name',
    )
    def __str__(self):
        return f'{self.title}'