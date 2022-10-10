from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  # se pueden agregar campos con related_name=""
  user = models.OneToOneField(User, on_delete = models.CASCADE)
  # image
  # pkmns

  def __str__(self):
    return f"{self.user.username}'s profile"