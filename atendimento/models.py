from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import json

class Usuario(models.Model):
    nome = models.TextField()

    def __str__(self):
        return self.nome

class Colaborador(models.Model):
    nome = models.TextField()

    def __str__(self):
        return self.nome

class Conversa(models.Model):
    usuarios = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    colaboradores = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    tag = models.TextField()

    def set_tag(self, x):
        self.tag = json.dumps(x) # No lugare de definir conversa.tag usa conversa.tag a variavel q o classificador retorna q eh um tuple 

    def get_tag(self):
        return json.loads(self.tag) ## retorna uma tuple c as duas tagas

    def __str__(self):
        return f"Conversa {self.id}"

class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    content = models.TextField()

    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')

    def __str__(self):
        return self.content
