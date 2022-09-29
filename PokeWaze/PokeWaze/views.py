from django.shortcuts import render
import pandas as pd

def home(request:str)->render:
    return render(request=request,
                  template_name="base/template_base.html")

def obtener_pokemon(request:str,pkmn:str)->render:
    """Entrega información sobre el Pokémon

    Args:
        request (str): Link.
        pkmn (str): Nombre de un Pokémon. 

    Returns:
        render: Genera la respuesta de la página Http con "Hello World".
    """
    # Generamos datos para la página
    df = pd.read_csv("https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv")
    df_filter = df[df["identifier"]==pkmn.lower()].reset_index().T
    
    data_pkmn = df_filter.to_dict()[0].items()
    
    # Agregamos las variables a traves de un diccionario al html
    # Subimos la página
    return render(request=request,
                  template_name="sala_pruebas.html",
                  context={"pkmn":data_pkmn,"name":pkmn})