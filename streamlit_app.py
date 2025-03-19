import streamlit as st
import requests

st.set_page_config(page_title="🔨 Craft Dofus 🔨", page_icon="⚒️")

st.title("🔨 Craft Dofus 🔨")
st.subheader("Recherche d'Items (Ressources & Équipements)")

# Recherche utilisateur
search_query = st.text_input("🔎 Recherche d'un item (ressource ou équipement) :", "")

# Fonction pour chercher des items (ressources + équipements)
def search_items(query):
    if not query:
        return []

    params = {
        "query": query,
        "limit": 10  # Tu peux augmenter si besoin
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

# Affiche la recette si elle existe
def show_recipe(item_id):
    # Utilisation de l'API pour obtenir la recette
    recipe_url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/search?filter[crafted_item.id]={item_id}"
    response = requests.get(recipe_url)

    if response.status_code == 200:
        data = response.json()

        # Si des recettes sont trouvées
        if data:
            st.success("✅ Recette disponible !")

            for item in data:
                st.markdown(f"➡️ **{item['name']}** (x{item['quantity']})")
                st.image(item['image_urls']['icon'], width=50)
                st.markdown(f"**Type :** {item['type']['name']}")
                st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")
        else:
            st.warning("❌ Aucune recette trouvée pour cet item.")
    else:
        st.error(f"Erreur API pour la recette : {response.status_code}")

# Si une recherche est faite :
if search_query:
    items = search_items(search_query)

    if not items:
        st.warning("Aucun résultat trouvé pour cette recherche.")
    else:
        st.subheader("📋 Résultats :")
        
        for item in items:
            with st.expander(f"{item['name']} (Lvl {item['level']})"):
                col1, col2 = st.columns([1, 3])

                with col1:
                    st.image(item['image_urls']['icon'], width=80)

                with col2:
                    st.markdown(f"**Nom :** {item['name']}")
                    st.markdown(f"**Niveau :** {item['level']}")
                    st.markdown(f"**Type :** {item['type']['name']}")
                    st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")
                    st.markdown(f"**Pods :** {item.get('pods', 'N/A')}")

                # Si l'item a une recette, afficher la recette
                if 'recipe' in item and item['recipe']:
                    st.markdown("---")
                    st.markdown("### 🧪 Recette de craft :")
                    show_recipe(item['ankama_id'])  # Passer l'ID de l'item pour récupérer la recette
                else:
                    st.info("Pas de recette disponible pour cet item.")
