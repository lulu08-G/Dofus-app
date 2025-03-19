import streamlit as st
import requests

st.set_page_config(page_title="🔨 Craft Dofus 🔨", page_icon="⚒️")

st.title("🔨 Craft Dofus 🔨")
st.subheader("Recherche et Recettes d'Items (Ressources uniquement pour les recettes)")

# Recherche utilisateur
search_query = st.text_input("🔎 Recherche d'une ressource craftable :", "")

# Fonction pour chercher des ressources
def search_resources(query):
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
def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.success("✅ Recette disponible !")

    for ingredient in recipe:
        item_id = ingredient['item_ankama_id']
        quantity = ingredient['quantity']
        subtype = ingredient['item_subtype']

        # Afficher les détails de chaque ingrédient
        st.markdown(f"➡️ **{quantity}x** [Item ID : `{item_id}`] - Type : {subtype}")
        
        # (Optionnel) Récupérer plus d'infos sur l'item si tu veux aller plus loin !

# Si une recherche est faite :
if search_query:
    resources = search_resources(search_query)

    if not resources:
        st.warning("Aucun résultat trouvé pour cette recherche.")
    else:
        st.subheader("📋 Résultats :")
        
        for item in resources:
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

                # Affiche la recette si disponible
                if 'recipe' in item and item['recipe']:
                    st.markdown("---")
                    st.markdown("### 🧪 Recette de craft :")
                    show_recipe(item['recipe'])
                else:
                    st.info("Pas de recette disponible pour cet item.")



