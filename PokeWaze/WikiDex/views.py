from django.shortcuts import render

# Create your views here.
import pandas as pd

def home(request:str)->render:
    return render(request=request,
                  template_name="template.html")

def obtener_pokemon(request:str)->render:
    """Entrega información sobre el Pokémon

    Args:
        request (str): Link.
        pkmn (str): Nombre de un Pokémon. 

    Returns:
        render: Genera la respuesta de la página Http con "Hello World".
    """
    
    
    # Request
    pkmn = request.GET["nameorid"]
    
    data_http = {} # Info a web
    
    # Generamos datos para la página
    df = pd.read_csv("https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv")
    
    # Checkeemos si el usuario entregó la id en vez del nombre
    if pkmn.isnumeric():
        df_filter = df[df["id"]==int(pkmn)].reset_index().T
    else:
        df_filter = df[df["identifier"]==pkmn.lower()].reset_index().T
    
    # si df_filter está vacío, el pokemon no es valido
    if df_filter.empty:
        return render(request=request,
                       template_name="404.html")
    # Obtener data e imagen
    data_pkmn = df_filter.to_dict()[0].items()
    id_pkmn = list(data_pkmn)[1][1]
    name_pkmn = list(data_pkmn)[2][1]
    
    # Agregamos las variables a traves de un diccionario al html
    # Subimos la página
    return render(request=request,
                  template_name="search.html",
                  context={"pkmn":data_pkmn,
                  "name":name_pkmn,
                  "id":id_pkmn,
                  "imageURL":f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id_pkmn}.png"})


