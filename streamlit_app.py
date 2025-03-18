import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

def search_items(query):
    """Rechercher des items par nom."""
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
    """Récupérer la recette d'un item par son ID."""
    # URL pour rechercher des recettes avec un item spécifique
    search_url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/search?filter%5Bitem_ankama_id%5D={item_id}"
    
    search_response = requests.get(search_url)

    if search_response.status_code != 200:
        st.error(f"Erreur recherche recette pour item {item_id} : {search_response.status_code}")
        return None

    recipes = search_response.json()

    if not recipes:
        st.warning(f"Aucune recette trouvée pour cet item.")
        return None

    return recipes

if search_query:
    items = search_items(search_query)

    st.subheader("📝 Résultats de recherche")
    for item in items:
        with st.expander(f"{item['name']} (Lvl {item['level']})"):
            st.image(item['image_urls']['icon'], width=100)

            if st.button(f"Voir la recette de {item['name']}", key=item['ankama_id']):
                # Appeler la fonction pour obtenir la recette
                recipe = get_recipe(item['ankama_id'])

                if recipe:
                    st.success(f"Recette pour {item['name']}")

                    # Afficher la recette sous forme d'ingrédients et quantités
                    for r in recipe:
                        if 'result' in r and 'ingredients' in r['result']:
                            for ingredient in r['result']['ingredients']:
                                ingr = ingredient['item']
                                qty = ingredient['quantity']

                                st.markdown(f"### {qty} x {ingr['name']}")
                                st.image(ingr['image_urls']['icon'], width=80)
                        else:
                            st.warning("Pas de recette disponible pour cet item !")
                else:
                    st.warning("Pas de recette disponible pour cet item !")
