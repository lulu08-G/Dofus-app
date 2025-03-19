import streamlit as st
import requests

st.set_page_config(page_title="🔨 Craft Dofus 🔨", page_icon="⚒️")

st.title("🔨 Craft Dofus 🔨")
st.subheader("Recherche d'Equipements")

# Recherche utilisateur
search_query = st.text_input("🔎 Recherche d'un équipement :", "")

# Fonction pour chercher des équipements
def search_items(query):
    if not query:
        return []

    params = {
        "query": query,
        "limit": 10  # Tu peux augmenter si besoin
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

# Fonction pour afficher la recette de l'item
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

# Fonction pour afficher les effets de l'item
def show_item_effects(effects):
    if not effects:
        st.warning("❌ Pas d'effets pour cet item.")
        return

    st.success("✅ Effets disponibles !")

    # Créer un tableau pour afficher les dégâts ou effets
    data = []
    for effect in effects:
        stat_type = effect['type']['name']
        min_damage = effect.get('int_minimum', 'N/A')
        max_damage = effect.get('int_maximum', 'N/A')
        formatted = effect.get('formatted', 'Aucun format')

        # Ajouter chaque effet sous forme de ligne
        data.append([stat_type, min_damage, max_damage, formatted])

    # Afficher sous forme de tableau
    st.table(data)

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

                # Affiche la recette si disponible
                if 'recipe' in item and item['recipe']:
                    st.markdown("---")
                    st.markdown("### 🧪 Recette de craft :")
                    show_recipe(item['recipe'])
                else:
                    st.info("Pas de recette disponible pour cet item.")

                # Afficher les effets si disponibles
                if 'effects' in item and item['effects']:
                    st.markdown("---")
                    st.markdown("### ⚡ Effets de l'item :")
                    show_item_effects(item['effects'])

