from turtle import title
from django.shortcuts import render
from django.http import JsonResponse
from pathlib import Path
import os
import requests

CVS_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("csv")

# Create your views here.
import pandas as pd

def home(request:str)->render:
    return render(request=request,
                  template_name="template.html")

def obtener_pokemon(request:str)->render:
    """Entrega información sobre el Pokémon

    Args:
        request (str): Link.

    Returns:
        render: Genera la respuesta de la página Http con "Hello World".
    """
    
    
    # Request
    pkmn_id = request.GET["nameorid"]
     
    # Generamos datos para la página
    df = pd.read_csv(os.path.join(CVS_DIR,"pokemon.csv"))
    
    # Checkeemos si el usuario entregó la id en vez del nombre
    if pkmn_id.isnumeric():
        df_filter = df[df["id"]==int(pkmn_id)].reset_index()
    else:
        df_filter = df[df["identifier"] == pkmn_id.replace(" ","-").lower()].reset_index()
    
    # si df_filter está vacío, el pokemon no es valido
    if df_filter.empty:
        return render(request=request,
                       template_name="404.html")
        
    # En caso que sea valido, crearemos un diccionario 
    # de la información obtenida del Pokémon.
    
    data_pkmn = df_filter.reset_index().T.to_dict()[0]
    
    # Vaciamos memoria extra
    del df
    del df_filter
    
    # pkmn_id (int): ID del Pokémon.
    pkmn_id = data_pkmn["id"] 
    
    # pkmn_name (str): Nombre del Pokémon.
    pkmn_name = data_pkmn["identifier"].replace("-"," ")
    pkmn_name = pkmn_name.title()
    
    # Obtener data útil del Pokémon
    for x in ["level_0","identifier","index"]:
        del data_pkmn[x]
        
    
    pkmn = [(feature.replace("_"," ").title(),value) for feature, value in data_pkmn.items()]
    
    # list_evolutions (list(str)): Lista de Evoluciones del Pokémon.
    
    list_evolutions = query_evolutions(pkmn_id)
    
    # list_forms (list(str)): Lista de otras formas del Pokémon.
    list_forms = list_evolutions["other"]
    
    # descripción del pkmn (quedan a la chucha)
    req = requests.get(f"https://www.pokemon.com/us/pokedex/{pkmn_name}/", 'html.parser')
    start_idx = req.text.find('<div class="version-descriptions active">')
    text = req.text[start_idx:start_idx+1000]
    req.close()
    pkmn_desc = text.split('\n')[5].strip() + '\n' + text.split('\n')[10].strip() if text.split('\n')[5].strip() != text.split('\n')[10].strip() else text.split('\n')[5].strip()
    del text

    # Agregamos las variables a traves de un diccionario al html
    # Subimos la página
    return render(request=request,
                  template_name="search.html",
                  context={"pkmn":pkmn,
                  "name":pkmn_name,
                  "formas": list_forms,
                  "before": list_evolutions["before"],
                  "after": list_evolutions["after"],
                  "id":pkmn_id,
                  "desc":pkmn_desc,
                  "imageURL":f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pkmn_id}.png"})


# obtener lista para el autocompletado
# maximo 13 resultados
def autosuggest(request):
    df = pd.read_csv(os.path.join(CVS_DIR,"pokemon.csv"))
    og_query = request.GET.get('term')
    query = og_query.lower()
    df = df[df["identifier"].str.contains(query)]
    df = df["identifier"].tolist()
    df = [x.replace("-"," ").title() for x in df]
    return JsonResponse(df[:13], safe=False)

############################## MÉTODOS AUXILIARES ###############################################

def query_forms(pkmn_id:int)->list:

    #Cargamos la base de datos a utilizar
    df_pkmn = pd.read_csv(os.path.join(CVS_DIR,"pokemon.csv"))
    df_pkmn_forms = pd.read_csv(os.path.join(CVS_DIR,"pokemon_forms.csv"))
    
    # Filtramos la información y la convertimos en listas
    df_filter1 = df_pkmn[df_pkmn["species_id"] == pkmn_id]["identifier"].to_list()
    df_filter2 = df_pkmn_forms[df_pkmn_forms["pokemon_id"] == pkmn_id]["identifier"].to_list()
    
    del df_pkmn_forms # Liberamos memoria
    
    # Unimos los identificadores de todas las formas de Pokémon buscado
    list_forms = set(df_filter1+df_filter2)
    list_forms.remove(df_pkmn[df_pkmn["id"]==pkmn_id]["identifier"].values[0])
    
    del df_pkmn, df_filter1, df_filter2 # Liberamos memoria
    
    return [(name.replace("-"," ").title(), identifier) for name,identifier in zip(list_forms,list_forms)]

def query_evolutions(pkmn_id:int)->dict:
    
    #Cargamos la base de datos a utilizar
    df_pkmn = pd.read_csv(os.path.join(CVS_DIR,"pokemon.csv"))
    df_pkmn_spe = pd.read_csv(os.path.join(CVS_DIR,"pokemon_species.csv"))
    
    #Obtenemos el id de la especie del Pokémon
    pkmn_spe_id = df_pkmn[df_pkmn["id"]==pkmn_id]["species_id"].values[0]
    
    #Obtenemos las otras formas
    pkmn_other = df_pkmn[df_pkmn["species_id"]==pkmn_spe_id]["identifier"].to_list()
    pkmn_other.remove(df_pkmn[df_pkmn["id"]==pkmn_id]["identifier"].values[0]) # Elimina al mismo Pokémon buscado
    
    del df_pkmn
    
    # Filtramos la información y la convertimos en listas
    df_filter1 = df_pkmn_spe[df_pkmn_spe["id"] == pkmn_spe_id]["evolution_chain_id"]
    df_filter2 = df_pkmn_spe[df_pkmn_spe["evolution_chain_id"] == df_filter1.values[0]]
    
    # Buscamos el order del Pokémon
    order = df_pkmn_spe[df_pkmn_spe["id"]==pkmn_spe_id]["order"].values[0]
    
    del df_pkmn_spe, pkmn_spe_id
    
    #Obtenemos las evoluciones
    pkmn_before = df_filter2[df_filter2["order"]<order]["identifier"].to_list()
    pkmn_after = df_filter2[df_filter2["order"]>order]["identifier"].to_list()
    
    del df_filter1, df_filter2
    
    return {"before": [(name.replace("-"," ").title(), identifier) for name,identifier in zip(pkmn_before,pkmn_before)],
            "after": [(name.replace("-"," ").title(), identifier) for name,identifier in zip(pkmn_after,pkmn_after)],
            "other": set([(name.replace("-"," ").title(), identifier) for name,identifier in zip(pkmn_other,pkmn_other)]
            + query_forms(pkmn_id=pkmn_id))
            }    
    
    
    del df_pkmn, df_filter1, df_filter2 # Liberamos memoria
    
    return [(name.replace("-"," ").title(), identifier) for name,identifier in zip(list_forms,list_forms)]
