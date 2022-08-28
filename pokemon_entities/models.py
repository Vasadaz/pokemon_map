from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_jp = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images', null=True)
    evolution = models.ForeignKey(
        'Pokemon',
        related_name='next_evolution',
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Pokemon',
        related_name='entities',
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(verbose_name='Latitude')
    long = models.FloatField(verbose_name='Longitude')
    appeared_at = models.DateTimeField(verbose_name='Appeared at', null=True)
    disappeared_at = models.DateTimeField(verbose_name='Disappeared at', null=True)
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.pokemon} on the map by ({self.lat}, {self.long})'
