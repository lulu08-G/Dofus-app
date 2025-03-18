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

def get_recipe_summary(item_ankama_id):
    # URL pour rechercher les recettes par l'ID de l'item
    url = "https://api.dofusdu.de/dofus3/v1/fr/recipes/search"
    
    # Paramètres de la requête pour chercher la recette
    params = {
        "filter[item_ankama_id]": item_ankama_id  # Recherche par l'ID de l'item
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipes = response.json()  # Récupérer la réponse sous forme de JSON
        
        if recipes:
            # Si des recettes sont trouvées, retourne le résumé
            recipe = recipes[0]  # Prendre la première recette disponible
            return {
                "item_ankama_id": recipe["item_ankama_id"],  # L'ID de l'item fabriqué
                "item_subtype": recipe["item_subtype"],      # Le sous-type de l'item (par exemple, "Équipement")
                "quantity": recipe["quantity"]                # La quantité nécessaire pour fabriquer l'item
            }
        else:
            return None  # Aucune recette trouvée pour cet item
    else:
        return None  # En cas d'erreur dans la requête

if search_query:
    items = search_items(search_query)

    st.subheader("📝 Résultats de recherche")
    for item in items:
        with st.expander(f"{item['name']} (Lvl {item['level']})"):
            st.image(item['image_urls']['icon'], width=100)

            # Affichage du résumé de la recette
            recipe_summary = get_recipe_summary(item['ankama_id'])
            if recipe_summary:
                st.write(f"Item à fabriquer : {recipe_summary['item_subtype']}")
                st.write(f"Quantité nécessaire : {recipe_summary['quantity']}")
                st.write(f"ID de l'item fabriqué : {recipe_summary['item_ankama_id']}")
            else:
                st.warning("Aucune recette disponible pour cet item !")
