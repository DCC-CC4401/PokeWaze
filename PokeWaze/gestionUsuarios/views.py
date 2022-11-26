from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
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
      username = form.cleaned_data["username"]
      messages.success(request, "Usuario creado exitosamente")
      return redirect(f'profile/{username}')
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
def user_profile(request:str, username:str)->render:
  all_users = User.objects.all()
  searchedUser = None
  for user in all_users:
    if user.username == username:
      searchedUser = user
  if searchedUser == None:
    return render(
      request,
      template_name="userNotFounded.html",
      context={
        "searched_username":username,
      }
    )
  return render(
    request,
    template_name="profile.html",
    context={
      "pkmn_list":[1,23,4]
    }
  )

@login_required
def edit_user_profile(request:str)->render:
  """ if request.method == "POST":
    form = UserRegisterForm(request.POST) # change to EditProfileForm
    if form.is_valid():
      form.save()
      username = form.cleaned_data["username"]
      messages.success(request, "Usuario creado exitosamente")
      return redirect(f'profile/{username}')
    else:
      messages.error(request, "Parámetros inválidos")
  else:
    form = UserRegisterForm() # change to EditProfileForm """
  return render(
    request,
    template_name="edit_profile.html", # cambiar a edit profile
    #context={
    #  "form":form
    #}
  )

@login_required
def list_of_users(request:str)->render:
  users_list = User.objects.all()
  return render(
    request,
    template_name="list_profiles.html",
    context={
      "pokewazers":users_list,
    }
  )

