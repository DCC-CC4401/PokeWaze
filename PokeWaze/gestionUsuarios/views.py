from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from gestionUsuarios.models import Feedback, Box, Pokemon, IdentifierNamePokemon
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
        """Usuario creado exitosamente. Vuelva a ingresar su Username y Password para ingresar"""
      )
      return redirect(f'../login')
    else:
      messages.error(request, "Parámetros inválidos")
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
  try:
    request.user.delete()
    messages.sucess(request, "The user has been successfully deleted.")
  except:
    messages.error(request, f"User '{request.user.username}' was not found")
  return render(request, 'deleted_user.html')

@login_required
def user_profile(request:str, aUsername:str)->render:
  try:
    searchedUser = User.objects.get(username = aUsername)
    searchPkmnList = list(Box.objects.filter(user_id=searchedUser.id))
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
      id_name = IdentifierNamePokemon.objects.get(name = name)
      search_poke = Pokemon.objects.get(identifier = id_name)
      newBox = Box(user_id = uid, pkmn_id = search_poke, lvl_pkmn = lvl, nickname_pkmn = nickname)
      newBox.save()
      messages.success(request, "Pokémon has been added successfully.")
      return redirect(f'../profile/{request.user.username}')
    except:
      messages.error(request, "The entered pokemon name does not exist in our databases.")
  return render(
    request=request,
    template_name="add_pkmn.html"
  )

@login_required
def del_pkmn(request:str)->render:
  if request.method=="POST":
    pkmn = request.POST["pokemon"]
    pkmn.delete()
    messages.success(request, "Pokémon has been deleted successfully.")
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
