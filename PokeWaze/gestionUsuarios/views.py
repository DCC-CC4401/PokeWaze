from django.shortcuts import render

# Create your views here.
def menu_usuarios(request:str)->render:
    return render(request=request,
                  template_name="menu.html")