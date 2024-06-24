from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200)
    image = models.ImageField('картинка')
    title_en = models.CharField('название(анг.)', max_length=200, blank=True)
    title_jp = models.CharField('название(яп.)', max_length=200, blank=True)
    description = models.TextField('описание', blank=True)
    previous_evolution = models.ForeignKey("self",
                                           verbose_name='предыдущая эволюция',
                                           on_delete=models.CASCADE,
                                           null=True, blank=True,
                                           related_name='next_evolutions')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    pokemon = models.ForeignKey(Pokemon,
                                verbose_name='покемон',
                                on_delete=models.CASCADE,
                                related_name='pokemon_entities')
    appeared_at = models.DateTimeField('появится', null=True, blank=True)
    disappeared_at = models.DateTimeField('пропадет', null=True, blank=True)
    level = models.IntegerField('уровень', null=True, blank=True)
    health = models.IntegerField('здоровье', null=True, blank=True)
    strenght = models.IntegerField('атака', null=True, blank=True)
    defence = models.IntegerField('защита', null=True, blank=True)
    stamina = models.IntegerField('выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon} {self.id}'
