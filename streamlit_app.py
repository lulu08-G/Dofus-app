def get_recipe(item_id):
    # 1. Search for recipe id
    search_url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/search?filter[item.id]={item_id}"
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        st.error(f"Erreur recherche recette pour item {item_id} : {search_response.status_code}")
        return None

    recipes = search_response.json()

    if not recipes:
        st.warning(f"Aucune recette trouvée pour cet item.")
        return None

    recipe_id = recipes[0]['id']

    # 2. Get recipe details
    recipe_url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/{recipe_id}"
    recipe_response = requests.get(recipe_url)

    if recipe_response.status_code != 200:
        st.error(f"Erreur récupération de la recette {recipe_id} : {recipe_response.status_code}")
        return None

    return recipe_response.json()
