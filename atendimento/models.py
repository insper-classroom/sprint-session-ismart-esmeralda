
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import CustomUser as User
import json
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from django import forms



class Conversa(models.Model):
    usuarios = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='colaborador')
    tag = models.TextField()
    resolved = models.BooleanField(default=False)
    is_zap = models.BooleanField(default=False)
    is_mail = models.BooleanField(default=False)


    def __str__(self):
        return f"Conversa {self.id}"

class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    content = models.TextField()

    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def update_response_time(self):
        #pega a ultima mensagem na conversa
        previous_message = Mensagem.objects.filter(conversa = self.conversa, id__lt = self.id).order_by('-id').first()

        if previous_message is not None:
            #calcula o tempo entre a mensagem atual e a anterior
            response_time = (self.timestamp - previous_message.timestamp).total_seconds()

            #atualiza a classe de stats

            stats = Stats.objects.first()
            if stats is None:
                stats = Stats.objects.create(total_response_time = response_time, total_response_count = 1)
            else:
                stats.total_response_time += response_time
                stats.total_response_count += 1
                stats.save()

    def __str__(self):
        return self.content

#decorator pra chamar o update stats toda vez q uma msg nova eh salva
@receiver(post_save, sender=Mensagem)
def update_response_time(sender, instance, **kwargs):
    instance.update_response_time()

class Stats(models.Model):
    sobreosismart = models.IntegerField(default=0)
    ismartonline = models.IntegerField(default=0)
    processoseletivo = models.IntegerField(default=0)
    bolsasdeestudo = models.IntegerField(default=0)
    totalresolvidos = models.IntegerField(default=0)
    total_response_time = models.FloatField(default=0)
    total_response_count = models.IntegerField(default=0)

    #propriedade pra calcular a media de tempo de resposta
    #eh um decorator q faz um metodo ser chamado como se fosse um atributo
    @property
    def average_response_time(self):
        if self.total_response_count == 0:
            return 0    
        return self.total_response_time / self.total_response_count
    
    
class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Assunto')
    message = forms.CharField(widget=forms.Textarea, label='Mensagem')

class Mail(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mails')
    content = models.TextField()
    subject = models.TextField()

    sender_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender = GenericForeignKey('sender_content_type', 'sender_object_id')
