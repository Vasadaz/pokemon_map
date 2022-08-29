from django.db import models


class Pokemon(models.Model):
    title = models.CharField(verbose_name='Имя рус.', max_length=200)
    title_en = models.CharField(verbose_name='Имя анг.', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Имя яп.', max_length=200, blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='images', null=True)
    next_evolution = models.ForeignKey(
        'Pokemon',
        verbose_name='Эволюция',
        related_name='previous_evolutions',
        blank=True,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        verbose_name='Покемон',
        related_name='entities',
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(verbose_name='Широта')
    long = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Появляется в')
    disappeared_at = models.DateTimeField(verbose_name='Исчезает в')
    level = models.IntegerField(verbose_name='Уровень')
    health = models.IntegerField(verbose_name='Здоровье', blank=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True)

    class Meta:
        verbose_name = 'Местонахождение покемона'
        verbose_name_plural = 'Местонахождение покемонов'

    def __str__(self):
        return f'{self.pokemon} on the map by ({self.lat}, {self.long})'
1