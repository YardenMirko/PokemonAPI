import requests

# Define the API endpoint URL 
Base_URL = 'https://pokeapi.co/api/v2/'

def test_pokemon_types():  
# Make a GET request to the API endpoint with a helper function
    endpoint = 'type'
    response = get_response(endpoint)
    
    data = response.json()
    expected_length = 20

# Check the response status code
    assert response.status_code == 200 , "Unexpected status code: " + str(response.status_code)

# Check that the response type
    assert isinstance(data, dict) , "Response is not a type JSON"

# Check that there are exactly 20 types.
    assert len(data['results']) == expected_length , "Expected 20 different Pokémon types"

def test_fire_type():   
    # Search for the fire type id with a helper function
    wanted_type = 'fire'
    wanted_type_id = get_type_id(wanted_type)
    assert wanted_type_id is not None, "Wanted type ID is not found"

    # Search for charmander in the fire Json list function - expected TRUE
    pokemon_check1 = 'charmander'
    temp1 = get_pokemon(pokemon_check1 , wanted_type_id)
    assert temp1 == True , "Charmander was not found on the fire type JSON list"

    # Search for bulbasaur in the fire Json list function - expected False
    pokemon_check2 = 'bulbasaur'
    temp2 = get_pokemon(pokemon_check2 , wanted_type_id)
    assert temp2 == False , "Bulbasaur was found on the fire type JSON list"

def test_heaviest_pokemons():
    wanted_type = 'fire'
    wanted_type_id = get_type_id(wanted_type)
    assert wanted_type_id is not None, "Wanted type ID is not found"

    expected_results = {
        'charizard-gmax': 10000,
        'cinderace-gmax': 10000,
        'coalossal-gmax': 10000,
        'centiskorch-gmax': 10000,
        'groudon-primal': 9997
    }

    # Search for five heaviest Pokémon of the Fire type with a helper function
    heavist = get_heaviest_pokemons(wanted_type_id)

    compare =  compare_results(expected_results, heavist)
    assert compare == True , "Unexpected results"

# Helper functions

def get_response(endpoint):
    return requests.get(f"{Base_URL}{endpoint}")
    
def get_type_id(wanted_type):
    response = get_response('type')
    data = response.json()
    for type in data['results']:
        if type['name'] == wanted_type:
            return type['url'].split('/')[-2]
    
    return None      
        
def get_pokemon(pokemon_name,wanted_type_id):
    endpoint ='type/'
    response = get_response(f'{endpoint}{wanted_type_id}')
    pokemons = response.json()

    for pokemon in pokemons['pokemon']:
        if pokemon_name == pokemon['pokemon']['name']:
            return True
    return False

def get_heaviest_pokemons(wanted_type_id):
    endpoint ='type/'
    response = get_response(f'{endpoint}{wanted_type_id}')
    pokemons = response.json()

    heaviest = {}
    min = 0

    for pokemon in pokemons['pokemon']:
       name = pokemon['pokemon']['name']
       weight = get_weight(name)
       if weight >= min:
           min = weight
           heaviest[name] = weight

    return dict(list(heaviest.items())[-5:]) 

def get_weight(pokemon_name):
    endpoint = 'pokemon/'
    response = get_response(f'{endpoint}{pokemon_name}')
    pokemon = response.json()
    return pokemon['weight']

def compare_results(dictionary1 , dictionary2):
    if len(dictionary1)!=len(dictionary2):
        return False
    if dictionary1== dictionary2:
        return True
    return False
    
