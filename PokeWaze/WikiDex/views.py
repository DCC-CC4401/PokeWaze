from turtle import title
from django.shortcuts import render
from WikiDex.models import *
from django.http import JsonResponse
from pathlib import Path
import os
import requests

CVS_DIR = Path(__file__).resolve().parent.parent.parent.joinpath("csv")

# Create your views here.
import pandas as pd

def home(request:str)->render:
    return render(request=request,
                  template_name="home.html")

def obtener_pokemon(request:str)->render:
    """Entrega información sobre el Pokémon

    Args:
        request (str): Nombre del pokemon.

    Returns:
        render: Genera la respuesta de la página Http con la información del Pokémon.
    """
    
    
    # Obtenemos el nombre del pkmn de la request
    pkmn_name = request.GET["nameorid"].title()
    
    # Realizamos la query en nuestra base de datos
    identifier_query = list(IdentifierNamePokemon.objects.filter(name=pkmn_name)) + list(FormsPokemon.objects.filter(pokemon_name=pkmn_name))
    
    # si identifier_query está vacío, el pokemon no es valido
    if len(identifier_query)==0:
        return render(request=request,
                       template_name="404.html")
    else:
        # En caso que sea valido, crearemos un diccionario 
        # de la información obtenida del Pokémon.
        data_pkmn = Pokemon.objects.get(identifier=identifier_query[0].__dict__["identifier"]).__dict__
    
        # pkmn_id (int): ID del Pokémon.
        pkmn_id = data_pkmn["id"]
    
        # list_evolutions (list(str)): Lista de Evoluciones del Pokémon.
        list_evolutions = query_evolutions(pkmn_id)
    
        # list_forms (list(str)): Lista de otras formas del Pokémon.
        list_forms = list_evolutions["other"]

        # Obtenemos la descripcion del pkmn por region
        pkmn_desc = DescriptionPokemon.objects.get(id=pkmn_id).__dict__
    
        # Eliminamos lo que no nos interesa
        del pkmn_desc["_state"], pkmn_desc["id"]
        aux = pkmn_desc.items()
        for version, text in aux:
            if text =="nan":
                del pkmn_desc[version]
        del aux

        for data in ['_state','id','identifier','species_id']:
            del data_pkmn[data]
    
        pkmn_stats = [(feature.replace("_"," ").title().replace(" ",""),value) for feature, value in data_pkmn.items()]
    
        # Agregamos las variables a traves de un diccionario al html
        # Subimos la página
        return render(request=request,
                    template_name="search.html",
                    context={"pkmn":pkmn_stats,
                    "name":pkmn_name,
                    "formas": list_forms,
                    "before": list_evolutions["before"],
                    "after": list_evolutions["after"],
                    "id":pkmn_id,
                    "desc":pkmn_desc.items(),
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

    # Filtramos la información y obtenemos los identificadores con los nombres
    df_identifier1 = list(map(lambda x: x.__dict__["identifier"],
                          FormsPokemon.objects.filter(pokemon_id=pkmn_id)))  
    df_identifier2 = list(map(lambda x: x.__dict__["identifier"],
                          Pokemon.objects.filter(species_id=pkmn_id)))
    
    # Filtramos la información y obtenemos listas con los nombres
    df_name1 = list(map(lambda x: x.__dict__["pokemon_name"],
                          FormsPokemon.objects.filter(pokemon_id=pkmn_id)))
    df_name2 = [IdentifierNamePokemon.objects.get(identifier=id).__dict__["name"] for id in df_identifier2]
    
    # Unimos los identificadores y nombres de todas las formas de Pokémon buscado
    list_forms_identifier = set(df_identifier1+df_identifier2)
    list_forms_names = set(df_name1+df_name2)
    
    # Removemos el pkmn buscado de ambas listas
    # Removiendo el identificador
    list_forms_identifier.remove(Pokemon.objects.get(id=pkmn_id).__dict__["identifier"])
    aux = Pokemon.objects.get(id=pkmn_id).__dict__["identifier"]
    # Removiendo el nombre
    list_forms_names.remove(IdentifierNamePokemon.objects.get(identifier=aux).__dict__["name"])
    
    del df_identifier1, df_identifier2, df_name1, df_name2, aux # Liberamos memoria
    
    return list(zip(list_forms_names,list_forms_identifier))

def query_evolutions(pkmn_id:int)->dict:
        
    #Obtenemos el id de la especie del Pokémon
    pkmn_spe_id = Pokemon.objects.get(id=pkmn_id).__dict__["species_id"]
    
    # Obtenemos las otras formas del pkmn
    # Obtenemos los identificadores
    pkmn_other_ident = list(map(lambda x: x.__dict__["identifier"],
                          Pokemon.objects.filter(species_id=pkmn_spe_id)))
    pkmn_other_ident.remove(Pokemon.objects.get(id=pkmn_id).__dict__["identifier"]) # Elimina al mismo Pokémon buscado
    # Obtenemos los nombres
    pkmn_other_names = [IdentifierNamePokemon.objects.get(identifier=id).__dict__["name"] for id in pkmn_other_ident]
    
    # Obteniendo la linea evolutiva
    # Obteniendo el id de la cadena evolutiva
    evo_chain_id = SpeciesPokemon.objects.get(id=pkmn_spe_id-1).__dict__["evolution_chain_id"]
    
    # Obteniendo la data base de la linea evolutiva
    df_evo = SpeciesPokemon.objects.filter(evolution_chain_id=evo_chain_id)
    
    # Buscamos el order del Pokémon
    pkmn_order = SpeciesPokemon.objects.get(id=pkmn_spe_id-1).__dict__["order"]
    
    del pkmn_spe_id
    
    #Obtenemos las evoluciones y sus nombres
    pkmn_before_ident = list(map(lambda x: x.__dict__["identifier"],
                           df_evo.filter(order__lt = pkmn_order)))
    pkmn_before_names = [IdentifierNamePokemon.objects.get(identifier=id).__dict__["name"] for id in pkmn_before_ident]
    
    pkmn_after_ident = list(map(lambda x: x.__dict__["identifier"],
                          df_evo.filter(order__gt = pkmn_order)))
    pkmn_after_names = [IdentifierNamePokemon.objects.get(identifier=id).__dict__["name"] for id in pkmn_after_ident]
    
    del pkmn_order, df_evo, evo_chain_id
    
    return {"before": list(zip(pkmn_before_names,pkmn_before_ident)),
            "after": list(zip(pkmn_after_names,pkmn_after_ident)),
            "other": set(list(zip(pkmn_other_names,pkmn_other_ident)) + query_forms(pkmn_id=pkmn_id))
            }