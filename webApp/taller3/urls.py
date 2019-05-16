from django.urls import path

from . import views

urlpatterns = [
    #path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('question/<id>', views.question, name='question'),
    path('lugar/<lugar>', views.lugar, name='lugar'),
]