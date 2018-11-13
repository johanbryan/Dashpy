from django.conf.urls import url

from . import views

#agrega un namespace para que django sepa que estas urls pertenecen
#all app con el nombre encuestas
app_name = 'encuestas'
urlpatterns = [ 
    #ejemplo /encuestas/
    url(r'^$', views.index, name='index'),
    #el name del final sirve para que el template lo invoque con {% url %} en el archivo html
    url(r'^especifico/(?P<pregunta_id>[0-9]+)/$', views.detalle, name='detalle'),
    
    url(r'^(?P<pregunta_id>[0-9]+)/resultado/$', views.resultado, name='resultado'),

    url(r'^(?P<pregunta_id>[0-9]+)/voto/$', views.voto, name='voto'),

    ]