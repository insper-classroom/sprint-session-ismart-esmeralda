from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
