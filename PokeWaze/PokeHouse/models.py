from django.db import models

# Create your models here.
class Caja(models.Model):
    user_id = models.IntegerField()
    pkmn_id = models.IntegerField()
    lvl_pkmn = models.IntegerField()
    
class IdentifierNamePokemon(models.Model):
    identifier = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

class TypePokemon(models.Model):
    type = models.CharField(max_length=50)

class Pokemon(models.Model):
    identifier = models.ForeignKey(IdentifierNamePokemon,null=False,blank=False, on_delete=models.CASCADE)
    species_id = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    hp = models.IntegerField()
    attack = models.IntegerField()
    sp_attack = models.IntegerField()
    defense = models.IntegerField()
    sp_defense = models.IntegerField()
    speed = models.IntegerField()
    type1_id = models.ForeignKey(TypePokemon,null=False,blank=False, on_delete=models.CASCADE)
    type2_id= models.ForeignKey(TypePokemon,null=False,blank=True, on_delete=models.CASCADE)

    def __str__(self)->str:
        