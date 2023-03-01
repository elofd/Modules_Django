from django.db import models


class Menu(models.Model):
    class Meta:
        ordering = ('position', )
        verbose_name = 'Пункт меню'
        verbose_name_plugal = 'Пункты меню'


    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.name)

