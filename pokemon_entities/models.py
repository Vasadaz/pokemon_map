from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images', null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Pokemon',
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(verbose_name='Latitude')
    long = models.FloatField(verbose_name='Longitude')

    def __str__(self):
        return f'{self.pokemon} on the map by ({self.lat}, {self.long})'
