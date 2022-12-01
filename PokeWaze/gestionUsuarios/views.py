from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from gestionUsuarios.models import Feedback, Box
from WikiDex.models import *
import datetime

def menu_usuarios(request:str)->render:
  return render(
    request=request,
    template_name="menu.html"
  )

def user_register(request:str)->render:
  if request.method == "POST":
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request,
        """New Account has been successfully created. Enter your username and password again to log in"""
      )
      return redirect(f'../login')
    else:
      messages.error(request, "Invalid parameters")
  else:
    form = UserRegisterForm()
  return render(
    request,
    template_name='register.html',
    context={
      "form":form
    }
  )

@login_required 
def delete_user(request):    
  if request.method == "POST":
    if request.POST["confirm"] == "yes":
      request.user.delete()
      messages.success(request, "Your Account has been successfully deleted")
      return redirect('../home')
    elif request.POST["confirm"] == "no":
      messages.success(request, "Your Account has not been deleted")
      return redirect(f'../profile/{request.user.username}')
  return render(request, 'pls_dont_go.html')

@login_required
def user_profile(request:str, aUsername:str)->render:
  try:
    searchedUser = User.objects.get(username = aUsername)
    searchPkmnList = list(Box.objects.filter(user_id=searchedUser.id))
    aux = []
    for x in searchPkmnList:
      try:
        aux.append((IdentifierNamePokemon.objects.get(identifier=Pokemon.objects.get(id=x.pkmn_id).identifier).name,x))
      except:
        aux.append((FormsPokemon.objects.get(identifier=Pokemon.objects.get(id=x.pkmn_id).identifier),x))    
    
    searchPkmnList = aux.copy()
    
    del aux
    
    return render(
      request,
      template_name="profile.html",
      context={
        "lookigUser":searchedUser,
        "pkmn_list":searchPkmnList,
      }
    )
  except:
    return render(
      request,
      template_name="userNotFounded.html",
      context={
        "searched_username":aUsername,
      }
    )

@login_required
def list_of_users(request:str)->render:
  sizes = {}
  users_list = User.objects.all()
  for user in users_list:
    sizes[user.username] = len(list(Box.objects.filter(user_id = user.id)))
  return render(
    request,
    template_name="list_profiles.html",
    context={
      "sizes":sizes,
    }
  )

@login_required
def add_pkmn(request:str)->render:
  if request.method=="POST":
    name = request.POST["pokemon_name"]
    nickname = request.POST["pokemon_nickname"]
    lvl = request.POST["pokemon_level"]
    uid = request.user.id
    try:
      list_identifier = list(IdentifierNamePokemon.objects.filter(name=name))
      list_identifier += list(FormsPokemon.objects.filter(pokemon_name=name))
      poke_id = Pokemon.objects.get(identifier = list_identifier[0].identifier).id
      try:
        newBox = Box(user_id = uid, pkmn_id = poke_id, lvl_pkmn = lvl, nickname_pkmn = nickname)
        newBox.save()
        messages.success(request, "Pokémon has been added successfully")
        return redirect(f'../profile/{request.user.username}')
      except:
        messages.error(request, "Invalid parameters.")
    except:
      messages.error(request, "The entered Pokémon name does not exist in our databases")
    
  return render(
    request=request,
    template_name="add_pkmn.html"
  )

@login_required
def del_pkmn(request:str)->render:
  if request.method=="POST":
    pkmnID = request.POST["pokemon"]
    #userID = request.user.id
    pkmn = Box.objects.get(id=int(pkmnID))
    pkmn.delete()
    messages.success(request, "Pokémon has been deleted successfully")
    return redirect(f'../profile/{request.user.username}')
  else:
    searchPkmnList = list(Box.objects.filter(user_id=request.user.id))
    return render(
      request=request,
      template_name="delete_pkmn.html",
      context={
        "pkmn_list":searchPkmnList,
      }
    )

@login_required
def menu_feedback(request:str)->render:
  if request.method=="POST":
    fb = request.POST["fb"]
    dt = datetime.date.today()
    uid = request.user.id
    newFB = Feedback(sender_id = uid, text = fb, created_at = dt)
    newFB.save()
    return render(request=request, template_name="feedbackSent.html")
  return render(
    request=request,
    template_name="feedback.html"
  )