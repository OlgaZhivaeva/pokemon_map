from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('название', max_length=200, blank=True)
    image = models.ImageField('картинка',null=True)
    title_en = models.CharField('название(анг.)',max_length=200, blank=True)
    title_jp = models.CharField('название(яп.)',max_length=200, blank=True)
    description = models.TextField('описание',max_length=1000, blank=True)
    previous_evolution = models.ForeignKey("self",
                                           verbose_name='предыдущая эволюция',
                                           on_delete=models.CASCADE,
                                           null=True, blank=True,
                                           related_name='next_evolution')

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    pokemon = models.ForeignKey(Pokemon, verbose_name='покемон', on_delete=models.CASCADE)
    appeared_at = models.DateTimeField('появится', null=True, blank=True)
    disappeared_at = models.DateTimeField('пропадет',null=True, blank=True)
    level = models.IntegerField('уровень')
    health = models.IntegerField('здоровье')
    strenght = models.IntegerField('атака')
    defence = models.IntegerField('защита')
    stamina = models.IntegerField('выносливость')

