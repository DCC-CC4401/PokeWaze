from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages


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