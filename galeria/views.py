# Responsável por exibir os conteúdos para o usuário

from django.shortcuts import render


def index(request):  # Responsável pela página principal da aplicação
    return render(request, 'galeria/index.html')

def imagem(request):
    return render(request, 'galeria/imagem.html')
