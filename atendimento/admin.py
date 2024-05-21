from django.contrib import admin
from .models import Conversa, Mensagem
from users.models import CustomUser

admin.site.register(Conversa)
admin.site.register(Mensagem)
admin.site.register(CustomUser)


# Register your models here.
