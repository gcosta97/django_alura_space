# Isola as urls relacionadas à esse app

from django.urls import path
from galeria.views import index, imagem, buscar

urlpatterns = [
    path('', index, name='home'),
    path('imagem/<int:foto_id>', imagem, name='imagem'),  # define que o url é composto também pelo id da foto, chama views.py
    path('buscar', buscar, name='buscar')
]
