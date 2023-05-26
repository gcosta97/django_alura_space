# Responsável por exibir os conteúdos para o usuário

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import unicodedata

from apps.galeria.models import Fotografia
from apps.galeria.forms import FotografiaForms, AprovarImagensForms

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
        fotografia.categoria = unicodedata.normalize("NFD", fotografia.categoria).encode("ascii", "ignore").decode("utf-8").lower()
    
    return fotografias

def buscar(request):
    
    if "buscar" in request.GET:
        nome_a_buscar = request.GET["buscar"]
        nome_a_buscar = unicodedata.normalize("NFD", nome_a_buscar).encode("ascii", "ignore").decode("utf-8").lower()
        ids_correspondentes = []

        if nome_a_buscar:
            fotografias_limpas = limpar_nomes_banco_pesquisa(Fotografia)

            for fotografia in fotografias_limpas:
                if nome_a_buscar in fotografia.nome or nome_a_buscar in fotografia.categoria:
                    ids_correspondentes.append(fotografia.id)

            fotografias = Fotografia.objects.filter(id__in = ids_correspondentes)

        else:
            fotografias = []

        
        return render(request, "galeria/index.html", {"cards": fotografias})

def nova_imagem(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return redirect('login')
    
    form = FotografiaForms
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Foto adicionada com sucesso. Aguardando aprovação.')
            return redirect('nova_imagem')

    return render(request, 'galeria/nova_imagem.html', {'form': form})

def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    form = FotografiaForms(instance=fotografia)

    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid:
            form.save()
            messages.success(request, 'Foto editada com sucesso.')
            return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

    return render(request, 'galeria/editar_imagem.html', {'form':form, 'foto_id':foto_id})

def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id=foto_id)
    fotografia.delete()
    messages.success(request, 'Foto excluída com sucesso.')
    return redirect('home')

def filtro(request, categoria):
    fotografias = Fotografia.objects.filter(publicada=True, categoria=categoria)

    return render(request, 'galeria/index.html', {"cards": fotografias, 'categoria':categoria})

def aprovar_imagens(request):
    if not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para acessar essa página')
        return redirect('login')
    
    imagens = Fotografia.objects.all()
    if request.method == 'POST':
        lista_ids = request.POST.getlist('boxes')
        
        imagens.update(publicada=False)

        imagens.filter(pk__in=lista_ids).update(publicada=True)

        messages.success(request, 'Alterações salvas com sucesso!')
        return redirect('home')

    
    return render(request, 'galeria/aprovar_imagens.html', {'imagens': imagens})
    