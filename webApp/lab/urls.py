from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rf2/', views.rf2, name='rf2'),
    path('rf1/', views.rf1, name='rf1'),
    path('rf3/', views.rf3, name='rf3'),
]