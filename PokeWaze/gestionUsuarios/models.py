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
  
class IdentifierNamePokemon(models.Model):
  identifier = models.CharField(max_length=50, primary_key=True)
  name = models.CharField(max_length=100)

class TypePokemon(models.Model):
  type = models.CharField(max_length=20, blank=True)
  
class Pokemon(models.Model):
  identifier = models.ForeignKey(IdentifierNamePokemon,null=False,blank=False,on_delete=models.CASCADE)
  id_species = models.IntegerField()
  height = models.IntegerField()
  weight = models.IntegerField()
  hp = models.IntegerField()
  attack = models.IntegerField()
  sp_attack = models.IntegerField()
  defense = models.IntegerField()
  sp_defense = models.IntegerField()
  speed = models.IntegerField()
  type1_id = models.IntegerField()
  type2_id = models.IntegerField()

class Box(models.Model):
  user_id = models.IntegerField()
  pkmn_id = models.ForeignKey(Pokemon,null=False,blank=False, on_delete=models.CASCADE)
  lvl_pkmn = models.IntegerField()
  nickname_pkmn = models.CharField(max_length=50)