from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass
    uuid = models.UUIDField(primary_key= True, default=uuid.uuid4, editable=False, unique=True)
# Create your models here.
