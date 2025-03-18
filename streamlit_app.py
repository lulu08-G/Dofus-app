import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

# Fonction pour rechercher des items
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

# Affiche les détails complets d'un item
def display_item_details(item):
    st.subheader(f"Détails de l'item : {item['name']}")
    st.write(f"**ID** : {item['ankama_id']}")
    st.write(f"**Type** : {item['type']['name']}")
    st.write(f"**Niveau** : {item['level']}")
    st.write(f"**Sous-type d'item** : {item['item_subtype']['name_id']}")
    st.write(f"**Description** : {item.get('description', 'Aucune description disponible')}")
    
    # Afficher l'image de l'item
    st.image(item['image_urls']['icon'], width=100)

    # Si disponible, afficher la recette de l'item
    recipe = get_recipe(item['ankama_id'])
    if recipe:
        st.write("Recette :")
        for ingredient in recipe.get("result", {}).get("ingredients", []):
            ingr = ingredient['item']
            qty = ingredient['quantity']
            st.markdown(f"- {qty} x {ingr['name']}")
            st.image(ingr['image_urls']['icon'], width=80)
    else:
        st.warning("Pas de recette disponible pour cet item.")

# Fonction pour récupérer la recette d'un item
def get_recipe(item_id):
    search_url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/search?filter[item_ankama_id]={item_id}"
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        st.error(f"Erreur recherche recette pour item {item_id} : {search_response.status_code}")
        return None

    recipes = search_response.json()

    if not recipes:
        st.warning(f"Aucune recette trouvée pour cet item.")
        return None

    return recipes[0]

# Si une recherche est effectuée
if search_query:
    items = search_items(search_query)

    st.subheader("📝 Résultats de recherche")
    for item in items:
        with st.expander(f"{item['name']} (Lvl {item['level']})"):
            display_item_details(item)
