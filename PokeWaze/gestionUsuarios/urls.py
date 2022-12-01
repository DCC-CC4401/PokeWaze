from django.contrib import admin
from django.urls import path
import WikiDex.views as wiki
import gestionUsuarios.views as user
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path("autosuggest/",wiki.autosuggest, name="autosuggest"),
]