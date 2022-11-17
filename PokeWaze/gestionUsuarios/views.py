from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
      print("good")
      return redirect(f'profile/{username}')
    else:
      messages.error(request, "Parámetros inválidos")
      print("bad")
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
def user_profile(request:str)->render:
  return render(
    request,
    template_name="profile.html",
  )