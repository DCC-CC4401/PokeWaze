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

class Feedback(models.Model):
  sender_id = models.IntegerField()
  text = models.CharField(max_length=100)
  created_at = models.DateField() 