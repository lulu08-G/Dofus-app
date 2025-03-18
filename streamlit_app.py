import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

def search_items(query):
    if not query:
        return []
    
    params = {
        "query": query,
        "limit": 5
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_recipe(item_id):
    # 1. Search for recipe id (correction de l'URL)
    search_url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/search?filter[item]={item_id}"
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

if search_query:
    items = search_items(search_query)

    st.subheader("📝 Résultats de recherche")
    for item in items:
        with st.expander(f"{item['name']} (Lvl {item['level']})"):
            st.image(item['image_urls']['icon'], width=100)

            if st.button(f"Voir la recette de {item['name']}", key=item['ankama_id']):
                recipe = get_recipe(item['ankama_id'])

                if recipe and "ingredients" in recipe.get('result', {}):
                    st.success(f"Recette pour {item['name']}")

                    for ingredient in recipe['result']['ingredients']:
                        ingr = ingredient['item']
                        qty = ingredient['quantity']

                        st.markdown(f"### {qty} x {ingr['name']}")
                        st.image(ingr['image_urls']['icon'], width=80)
                else:
                    st.warning("Pas de recette disponible pour cet item !")
