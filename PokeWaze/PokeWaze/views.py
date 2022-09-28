from django.http import HttpResponse
import pandas as pd

def saludo(request:str)->HttpResponse:
    """Saludar

    Args:
        request (str): Link.

    Returns:
        HttpResponse: Genera la respuesta de la página Http con "Hello World".
    """
    return HttpResponse("Hello World")

def obtener_pokemon(request:str,pkmn:str)->HttpResponse:
    """Entrega información sobre el Pokémon

    Args:
        request (str): Link.
        pkmn (str): Nombre de un Pokémon. 

    Returns:
        HttpResponse: Genera la respuesta de la página Http con "Hello World".
    """
    df = pd.read_csv("https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv")
    df_filter = df[df["identifier"]==pkmn.lower()]

    return HttpResponse(df_filter.T.to_html(header=False))
