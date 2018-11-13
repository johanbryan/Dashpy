# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Pregunta(models.Model):
    pregunta_texto = models.CharField(max_length=200)
    publicacionfecha = models.DateTimeField('fecha publicado')

    def __str__(self):
        return self.pregunta_texto

@python_2_unicode_compatible
class Seleccion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
    seleccion_texto = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.seleccion_texto
    