import streamlit as st
import requests
import json

st.title("🔨 Recherche de Recette Dofus 🔨")

# Entrée de l'ID de l'item
item_id = st.text_input("Entre l'ID de l'item pour voir ses ressources de craft :")

def get_recipe_resources(item_id):
    url = "https://api.dofusdu.de/dofus3/v1/fr/items/resources/search"
    params = {
        "query": "",
        "filter[crafted_item.id]": item_id
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur : {response.status_code}")
        st.error(response.text)
        return None

# Quand un ID est renseigné :
if item_id:
    st.info(f"Recherche des composants pour l'item ID {item_id}...")
    recipe_data = get_recipe_resources(item_id)

    if recipe_data and len(recipe_data) > 0:
        st.success(f"Composants trouvés pour l'item ID {item_id} :")

        # Boucle sur chaque ressource dans la recette
        for resource in recipe_data:
            st.markdown(f"### {resource['name']}")
            st.image(resource['image_urls']['icon'], width=80)
            st.write(f"Type : {resource['type']['name']}")
            st.write(f"Niveau : {resource['level']}")
            st.write(f"ID Ankama : {resource['ankama_id']}")
            st.divider()

    else:
        st.warning("Aucune ressource trouvée pour cet item !")

