# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404

from django.shortcuts import get_object_or_404
from django.shortcuts import render

import hairball
import os

from django.http import HttpResponse
from django.template import loader

from .models import Pregunta

# Create your views here.

def perceptivos(request):
    album = {}
    """ pasale el contexto o el output de criterios perceptivos a la vista para usarla en la plantilla """
    comando = "hairball  -p perceptivos.Mecanica -p perceptivos.Dialogos -p perceptivos.Eventos -p perceptivos.Puntuacion -p perceptivos.Acciones -p perceptivos.Objetivo " + os.path.expanduser("~/Desktop/scratch")
    resultado = os.popen(comando).read()
    """
    lineas = resultado.splitlines()
    lineas.pop(0)
    #agregando los criterios al contexto segun el mismo orden en el que se agrgan en el comando
    #mecanica dialogos eventos puntuacion acciones objetivo
    
    contexto = { 'criterio1color' : lineas[0],
                 'criterio1comen' : lineas[1],
                 'criterio1canti' : lineas[2],
                 'criterio2color' : "empty",
                 'criterio2comen' : "empty",
                 'criterio2canti' : "empty",
                 'criterio3color' : lineas[3],
                 'criterio3comen' : lineas[4],
                 'criterio3canti' : lineas[5],
                 'criterio4color' : lineas[6],
                 'criterio4comen' : lineas[7],
                 'criterio4canti' : lineas[8],
                 'criterio5color' : lineas[9],
                 'criterio5comen' : lineas[10],
                 'criterio5canti' : lineas[11],
                 'criterio6color' : lineas[12],
                 'criterio6comen' : lineas[13],
                 'criterio6canti' : lineas[14], 
                 'criterio7color' : lineas[15],
                 'criterio7comen' : lineas[16],
                 'criterio7canti' : lineas[17],
     }"""
    return render(request, 'encuestas/perceptivos.html', resultado)

def index(request):
    ultima_pregunta_lista = Pregunta.objects.order_by('-publicacionfecha')[:5]
    template = loader.get_template('encuestas/index.html')
    context = {'ultima_pregunta_lista' : ultima_pregunta_lista }
    return HttpResponse(template.render(context, request))
    ##otra forma de hacerlo sin httpresponse es con render
    # return render(request, 'encuestas/index.html', context) 

def detalle(request, pregunta_id):
    pregunta = get_object_or_404(Pregunta, pk=pregunta_id)
    return render(request, 'encuestas/detalle.html', {'pregunta': pregunta})
    #try: 
     #   pregunta = Pregunta.objects.get(pk=pregunta_id)
    #except Pregunta.DoesNotExist:
     #   raise Http404('esta pregunta no existe en detalle')
    #return render(request, 'encuestas/detalle.html', {'pregunta' : pregunta})        
    # esto es una alternativa para saber si responde
    # return HttpResponse('esto es detalle tu estas viendo la pregunta %s.' %pregunta_id)

def resultado(request, pregunta_id):
    respuesta = "esto es resultado tu estas viendo los resultados de la pregunta %s."
    return HttpResponse(respuesta % pregunta_id)

def voto(request, pregunta_id):
    return HttpResponse("esto es voto tu estas votando en la pregunta %s." %pregunta_id)