from turtle import title
from django.shortcuts import render
from WikiDex.models import *
from django.http import JsonResponse

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
    pkmn_name = request.GET["nameorid"]
    
    # Realizamos la query en nuestra base de datos
    name_query = list(IdentifierNamePokemon.objects.filter(name=pkmn_name))
    name_query += list(FormsPokemon.objects.filter(pokemon_name=pkmn_name))
    identifier_list = list(set(list(map(lambda x: x.identifier,name_query))))
    
    # si name_query está vacío, el pokemon no es valido
    if len(identifier_list)==0:
        return render(request=request,
                       template_name="404.html")
    else:
        
        pkmn_identifier = identifier_list[0]       
        
        # En caso que sea valido, crearemos un diccionario 
        # de la información obtenida del Pokémon.
        try:
            image_ID = FormsPokemon.objects.get(identifier=pkmn_identifier).pokemon_id
            data_pkmn = Pokemon.objects.get(id=image_ID).__dict__
            
        except:
            data_pkmn = Pokemon.objects.get(identifier=pkmn_identifier).__dict__
            # pkmn_id (int): image_ID del Pokémon.
            image_ID = data_pkmn["id"]

        # list_evolutions (list(str)): Lista de Evoluciones del Pokémon.
        list_evolutions = query_evolutions(data_pkmn["id"],pkmn_name)
    
        # list_forms (list(str)): Lista de otras formas del Pokémon.
        list_forms = list_evolutions["other"]

        # Obtenemos la descripcion del pkmn por region
        pkmn_desc = DescriptionPokemon.objects.get(id=data_pkmn["species_id"]).__dict__
    
        # Eliminamos lo que no nos interesa en las descripciones
        del pkmn_desc["_state"], pkmn_desc["id"]
        
        aux = []
        for version, text in pkmn_desc.items():
            if text =="nan":
                aux.append(version)
        
        for version in aux:
            del pkmn_desc[version]

        # Eliminando data innecesaria del pkmn
        for data in ['_state','id','identifier','species_id']:
            del data_pkmn[data]
        
        if data_pkmn["type2"]=="nan":
            del data_pkmn["type2"]
    
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
                    "id":image_ID,
                    "desc":pkmn_desc.items(),
                    "alt": pkmn_name,
                    "imageURL":f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{image_ID}.png"})


# obtener lista para el autocompletado
# maximo 13 resultados
def autosuggest(request):
    og_query = request.GET.get('term')
    query = og_query.lower()
    df = list(map(lambda x: x.name, IdentifierNamePokemon.objects.filter(name__icontains=query)))
    df += list(map(lambda x: x.pokemon_name, FormsPokemon.objects.filter(pokemon_name__icontains=query)))
    return JsonResponse(df[:5], safe=False)

############################## MÉTODOS AUXILIARES ###############################################

def query_forms(pkmn_id:int,pkmn_name:str)->list:
    # Obtenemos la id de la especie
    pkmn_spe_id = Pokemon.objects.get(id=pkmn_id).species_id

    # Filtramos la información y obtenemos los identificadores con los nombres
    df_name1 = list(map(lambda x: x.pokemon_name,
                        FormsPokemon.objects.filter(pokemon_id=pkmn_id)))
    df_name2 = list(map(lambda x: IdentifierNamePokemon.objects.get(identifier=x.identifier).name,
                    Pokemon.objects.filter(species_id=pkmn_spe_id)))
    
    # Unimos los identificadores y nombres de todas las formas de Pokémon buscado
    list_forms_names = list(set(df_name1+df_name2))
    
    # Removemos el pkmn buscado de ambas listas
    # Removiendo el identificador
    if pkmn_name in list_forms_names:
        list_forms_names.remove(pkmn_name)
    
    if "nan" in list_forms_names:
        list_forms_names.remove("nan")
    
    del df_name1, df_name2 # Liberamos memoria
    
    return list_forms_names

def query_evolutions(pkmn_id:int,pkmn_name:str)->dict:
        
    #Obtenemos el id de la especie del Pokémon
    pkmn_spe_id = Pokemon.objects.get(id=pkmn_id).species_id
    
    # Obtenemos las otras formas del pkmn
    # Obtenemos los identificadores
    pkmn_other_names = []
    for x in Pokemon.objects.filter(species_id=pkmn_spe_id):
        if "nan" in list(FormsPokemon.objects.filter(identifier=x.identifier)):
            pkmn_other_names.append(FormsPokemon.objects.get(identifier=x.identifier).pokemon_name)
        else:
            pkmn_other_names.append(IdentifierNamePokemon.objects.get(identifier=x.identifier).name)

    # Removemos el pkmn buscado
    # Removiendo el nombre
    if pkmn_name in pkmn_other_names:
        pkmn_other_names.remove(pkmn_name)
    
    if "nan" in pkmn_other_names:
        pkmn_other_names.remove("nan")
        
    # Obteniendo la linea evolutiva
    # Obteniendo el id de la cadena evolutiva
    aux = SpeciesPokemon.objects.get(id=pkmn_spe_id-1)
    
    evo_chain_id = aux.evolution_chain_id
    
    # Obteniendo la data base de la linea evolutiva
    df_evo = SpeciesPokemon.objects.filter(evolution_chain_id=evo_chain_id)
    
    # Buscamos el order del Pokémon
    pkmn_order = aux.order
    
    del pkmn_spe_id, aux
    
    #Obtenemos las evoluciones y sus nombres
    
    pkmn_before_names = []
    for x in df_evo.filter(order__lt = pkmn_order):
        if "nan" in list(FormsPokemon.objects.filter(identifier=x.identifier)):
            pkmn_before_names.append(FormsPokemon.objects.get(identifier=x.identifier).pokemon_name)
        else:
            pkmn_before_names.append(IdentifierNamePokemon.objects.get(identifier=x.identifier).name)
    
    
    pkmn_after_names = []
    for x in df_evo.filter(order__gt = pkmn_order):
        if "nan" in list(FormsPokemon.objects.filter(identifier=x.identifier)):
            pkmn_after_names.append(FormsPokemon.objects.get(identifier=x.identifier).pokemon_name)
        else:
            pkmn_after_names.append(IdentifierNamePokemon.objects.get(identifier=x.identifier).name)

    del pkmn_order, df_evo, evo_chain_id
    
    return {"before": pkmn_before_names,
            "after": pkmn_after_names,
            "other": set(pkmn_other_names + query_forms(pkmn_id=pkmn_id,pkmn_name=pkmn_name))
            }
