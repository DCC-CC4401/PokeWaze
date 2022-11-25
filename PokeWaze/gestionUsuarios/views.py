from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from gestionUsuarios.models import Feedback
import datetime


# Create your views here.
def menu_usuarios(request:str)->render:
  return render(
    request=request,
    template_name="menu.html"
  )

def user_register(request:str)->render:
  if request == "POST":
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data["username"]
      messages.success(request, f"Usuario creado exitosamente")
      return redirect("home")
  else:
    form = UserRegisterForm()
  return render(
    request=request,
    template_name='register.html',
    context={
      "form":form
    }
  )

def user_profile(request:str, username:str)->render:
  if False:
    temp = "profile.html"
  else:
    temp = "userNotFounded.html"
  return render(
    request=request,
    template_name=temp,
    context={
      "username":username
    }
  )

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