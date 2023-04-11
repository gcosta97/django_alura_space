# Criação das tabelas do BD. classes representam as tabelas e as instâncias suas linhas.
# Assim que for criada a classe, precisam ser rodados dois comandos:
#   |-> 'python manage.py makemigrations': O comando makemigrations cria novas migrações com base nas alterações detectadas nos modelos.
#   |-> 'python manage.py migrate': O comando migrate sincroniza o estado do banco de dados com o conjunto atual de modelos e migrações.
# Sempre que houver alguma alteração nos models, fazer a migration novamente

from django.db import models
import unicodedata

class Fotografia(models.Model):
    # Os atributos representam as colunas do BD

    OPCOES_CATEGORIA = [
        ("NEBULOSA", "Nebulosa"),
        ("ESTRELA", "Estrela"),
        ("GALÁXIA", "Galáxia"),
        ("PLANETA", "Planeta")
    ]

    nome = models.CharField(max_length=100, null=False, blank=False)
    legenda = models.CharField(max_length=150, null=False, blank=False)
    descricao = models.TextField(null=False, blank=False)
    categoria = models.TextField(max_length=100, choices=OPCOES_CATEGORIA, default='')
    foto = models.ImageField(upload_to="fotos/%Y/%m/%d/", blank=True)
    publicada = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
