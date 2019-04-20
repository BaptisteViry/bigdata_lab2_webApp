from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('presentacionDB/', views.presentacionDB, name='presentacionDB'),
    path('charts/', views.charts, name='charts'),
    path('hashtagWordCloud/', views.hashtagWordCloud, name='hashtagWordCloud'),
    path('toptuiteros/',views.getTopTuiteros,name='toptuiteros'),
    path('palabrasclave/',views.getPalabrasClave,name='palabrasclave'),
    path('polaridad/<coleccion>/<screen_name>/',views.getPolaridadCuenta,name='polaridad'),
    path('apoyo/',views.getApoyoGeneral,name='apoyo'),
    path('apoyocuenta/<coleccion>/<screen_name>/',views.getApoyoCuenta,name='apoyocuenta'),
    path('toplugares/',views.getTopLugares,name='toplugares'),
]