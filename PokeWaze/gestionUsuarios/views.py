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
def user_profile(request:str)->render:
  return render(
    request,
    template_name="profile.html",
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