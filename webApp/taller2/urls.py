from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('presentacionDB/', views.presentacionDB, name='presentacionDB'),
    path('charts/', views.charts, name='charts'),
    path('hashtagWordCloud/', views.hashtagWordCloud, name='hashtagWordCloud'),
    path('toptuiteros/',views.getTopTuiteros,name='toptuiteros'),
    path('palabrasclave/',views.getPalabrasClave,name='palabrasclave')
]