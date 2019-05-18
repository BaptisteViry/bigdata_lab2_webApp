from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('question/<id>', views.question, name='question'),
    path('lugar/<lugar>', views.lugar, name='lugar'),
    path('map/<lugar>', views.map, name='map'),
    path('persona/<persona>',views.persona,name='persona'),
    path('buscartopic/<topic>',views.buscartopic,name='buscartopic'),
]