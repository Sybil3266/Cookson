from django.db import models

# Create your models here.

class Recipe(models.Model):
    name = models.CharField(verbose_name='음식명', max_length=20, unique=True)
    recipe = models.TextField(verbose_name='요리법')
    image = models.ImageField(null=True, verbose_name='사진')

    def __str__(self):
        return self.name