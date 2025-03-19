import streamlit as st
import requests

st.set_page_config(page_title="🔍 Recherche Items Dofus", layout="centered")
st.title("🔍 Recherche d'équipements Dofus")

API_BASE_URL = "https://api.dofusdu.de/dofus3/v1/fr"

# Fonction de recherche d'items équipements
def search_items(query):
    if not query:
        return []
    
    params = {
        "query": query,
        "limit": 10
    }

    url = f"{API_BASE_URL}/items/equipments/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        items = response.json()
        return items
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

# Fonction pour récupérer les ressources de craft (hypothèse recette)
def get_recipe_resources(item_id):
    url = f"{API_BASE_URL}/items/resources/search?filter[crafted_item.id]={item_id}"
    response = requests.get(url)

    if response.status_code == 200:
        resources = response.json()
        return resources
    else:
        st.warning(f"Aucune ressource trouvée pour la recette de l'item {item_id} (code {response.status_code})")
        return None

# Fonction pour afficher les détails d'un item
def show_item_details(item):
    st.header(f"{item.get('name')} (Niveau {item.get('level')})")
    st.image(item['image_urls']['icon'], width=150)

    st.markdown("### Informations principales")
    st.markdown(f"**ID Ankama** : {item.get('ankama_id')}")
    st.markdown(f"**Type** : {item['type'].get('name')}")
    st.markdown(f"**Sous-Type** : {item['item_subtype'].get('name_id')}")

    st.markdown("### Description")
    st.info(item.get('description', "Pas de description disponible."))

    # Récupérer et afficher les ressources de craft
    recipe_resources = get_recipe_resources(item['id'])  # ou item['ankama_id'] selon l'API

    if recipe_resources:
        st.subheader("🔨 Recette (Ressources nécessaires)")
        for resource in recipe_resources:
            st.markdown(f"- {resource.get('name')} (Niveau {resource.get('level')})")
            st.image(resource['image_urls']['icon'], width=80)
    else:
        st.warning("Aucune recette disponible pour cet item !")

# ============================
# MAIN
# ============================
search_query = st.text_input("Recherche d'un équipement :", "")

if search_query:
    items = search_items(search_query)

    if items:
        st.subheader("📋 Résultats de recherche")
        for item in items:
            if st.button(f"{item['name']} (Lvl {item['level']})", key=item['id']):
                show_item_details(item)
    else:
        st.info("Aucun résultat trouvé pour cette recherche.")

