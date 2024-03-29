from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from gestionUsuarios.models import Feedback, Box
import datetime


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
def user_profile(request:str, aUsername:str)->render:
  all_users = User.objects.all()
  searchedUser = None
  for aUser in all_users:
    if aUser.username == aUsername:
      searchedUser = aUser
  if searchedUser == None:
    return render(
      request,
      template_name="userNotFounded.html",
      context={
        "searched_username":aUsername,
      }
    )
  searchId = searchedUser.id
  all_boxes = Box.objects.all()
  searchPkmnList = []
  for box in all_boxes:
    if box.user_id == searchId:
      searchPkmnList.append(box)
  return render(
    request,
    template_name="profile.html",
    context={
      "lookigUser":searchedUser,
      "pkmn_list":searchPkmnList,
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
    template_name="edit_profile.html",
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

@login_required
def add_pkmn(request:str)->render:
  return render(
    request=request,
    template_name="add_pkmn.html"
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
  if request.user.is_authenticated:
    return render(
      request=request,
      template_name="feedback.html"
    )
  return redirect("../login/")
