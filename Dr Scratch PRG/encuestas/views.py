# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404

from django.shortcuts import get_object_or_404
from django.shortcuts import render


from django.http import HttpResponse
from django.template import loader

from .models import Pregunta

# Create your views here.

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