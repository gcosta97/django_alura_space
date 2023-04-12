# Responsável por exibir os conteúdos para o usuário

from django.shortcuts import render, get_object_or_404
import unicodedata

from galeria.models import Fotografia

def index(request):  # Responsável pela página principal da aplicação
    fotografias = Fotografia.objects.filter(publicada=True)
    return render(request, 'galeria/index.html',{"cards": fotografias})

# Pega o objeto no banco com a chave primária igual ao foto_id e passa para o imagem.html
def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def limpar_nomes_banco_pesquisa(nome_banco):
    fotografias = nome_banco.objects.filter(publicada=True)

    for fotografia in fotografias:
        fotografia.nome = unicodedata.normalize("NFD", fotografia.nome).encode("ascii", "ignore").decode("utf-8").lower()
    
    return fotografias

def buscar(request):
    
    if "buscar" in request.GET:

        nome_a_buscar = request.GET["buscar"]
        nome_a_buscar = unicodedata.normalize("NFD", nome_a_buscar).encode("ascii", "ignore").decode("utf-8").lower()
        ids_correspondentes = []

        if nome_a_buscar:
            fotografias_limpas = limpar_nomes_banco_pesquisa(Fotografia)

            for fotografia in fotografias_limpas:
                if nome_a_buscar in fotografia.nome:
                    ids_correspondentes.append(fotografia.id)

            fotografias = Fotografia.objects.filter(id__in = ids_correspondentes)

        else:
            fotografias = []

        
        return render(request, "galeria/buscar.html", {"cards": fotografias})
