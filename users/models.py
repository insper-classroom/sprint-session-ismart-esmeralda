from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_colaborador = models.BooleanField(default=False)
# Create your models here.
