"""PokeWaze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import WikiDex.views as wiki
import gestionUsuarios.views as user
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/", wiki.home, name="home"),
    path("info/<str:pkmn>", wiki.obtener_pokemon),
    path("info/", wiki.obtener_pokemon, name="buscar"),
    path("menu/", user.menu_usuarios, name="menu_user"),
    path("register/", user.user_register, name="registro"),
    path("profile/", user.user_profile, name="perfil"),
    path("profile/<str:aUsername>", user.user_profile, name="perfil_de_usuario"),
    path("profile/edit/", user.edit_user_profile, name="editar_perfil"),
    path("profiles/", user.list_of_users, name="perfiles"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True, template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("update_box/",user.add_pkmn, name="add_a_pkmn"),
    path("feedback/", user.menu_feedback, name="feedback"),
    path("autosuggest/",wiki.autosuggest, name="autosuggest"),
]
