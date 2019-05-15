from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('pantalla1/', views.pantalla1, name='pantalla1'),
]