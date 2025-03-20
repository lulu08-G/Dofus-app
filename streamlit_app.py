import streamlit as st
import requests
import json

# Personnalisation du thème Streamlit (Dark Theme en cohérence avec DofusBook)
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: #f0f0f0;
    }
    .stButton>button {
        color: white;
        background-color: #4CAF50;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .stExpander {
        background-color: #2a2a2a;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔨 Craft Dofus - Dark Mode 🔨")

# Recherche d'un item
search_query = st.text_input("🔎 Recherche d'un équipement :", "")

# ======================
# Recherche d'items
# ======================
def search_items(query):
    if not query:
        return []

    params = {
        "query": query,
        "limit": 5
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/search"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("❌ Erreur de formatage JSON : réponse invalide.")
            st.text(response.text)
            return []
    else:
        st.error(f"❌ Erreur API : {response.status_code}")
        return []

# ======================
# Détails de l'item Équipement
# ======================
def get_equipment_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/equipment/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("❌ Erreur JSON dans les détails de l'équipement.")
            st.text(response.text)
            return {}
    else:
        st.error(f"❌ Erreur API : {response.status_code}")
        return {}

# ======================
# Détails de la ressource (pour la recette)
# ======================
def get_resource_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("❌ Erreur JSON dans les détails de la ressource.")
            st.text(response.text)
            return {}
    else:
        st.error(f"❌ Erreur API : {response.status_code}")
        return {}

# ======================
# Affichage de la recette
# ======================
def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.markdown("### 🧪 Recette de craft :")
    for ingredient in recipe:
        item_id = ingredient['item_ankama_id']
        quantity = ingredient['quantity']

        # Récupérer les détails de la ressource associée
        resource_details = get_resource_details(item_id)

        resource_name = resource_details.get('name', 'Nom indisponible')
        image_url = resource_details.get('image_urls', {}).get('icon', '')

        col1, col2, col3 = st.columns([1, 1, 6])

        with col1:
            st.markdown(f"**{quantity}x**")

        with col2:
            if image_url:
                st.image(image_url, width=40)
            else:
                st.text("❓")

        with col3:
            st.markdown(f"**{resource_name}**")

# ======================
# Affichage des statistiques
# ======================
def show_item_stats(item):
    st.markdown("### 📊 Statistiques :")

    stats = item.get('effects', [])

    if not stats:
        st.warning("❌ Aucune statistique disponible pour cet item.")
        return

    data = []
    for stat in stats:
        stat_type = stat['type']['name']
        min_value = stat.get('int_minimum', 'N/A')
        max_value = stat.get('int_maximum', 'N/A')
        formatted = stat.get('formatted', 'N/A')

        data.append({
            "Type": stat_type,
            "Min": min_value,
            "Max": max_value,
            "Description": formatted
        })

    st.table(data)

# ======================
# Affichage principal
# ======================
if search_query:
    items = search_items(search_query)

    if not items:
        st.warning("❌ Aucun résultat trouvé pour cette recherche.")
    else:
        st.subheader("📋 Résultats :")

        for item in items:
            if 'name' in item and 'level' in item:
                with st.expander(f"{item['name']} (Lvl {item['level']})"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        st.image(item['image_urls']['icon'], width=80)

                    with col2:
                        st.markdown(f"**📝 Nom :** {item['name']}")
                        st.markdown(f"**🔢 Niveau :** {item['level']}")
                        st.markdown(f"**🎭 Type :** {item['type']['name']}")
                        st.markdown(f"**📄 Description :** {item.get('description', 'Aucune description disponible.')}")

                    # Détails supplémentaires
                    item_details = get_equipment_details(item['ankama_id'])

                    # Recette
                    if 'recipe' in item_details and item_details['recipe']:
                        show_recipe(item_details['recipe'])
                    else:
                        st.info("ℹ️ Pas de recette pour cet item.")

                    # Stats
                    show_item_stats(item_details)

                    # Autres infos
                    st.markdown("### 🔧 Informations supplémentaires :")
                    st.markdown(f"**📦 Pods :** {item_details.get('pods', 'N/A')}")
                    st.markdown(f"**🔐 Conditions :** {item_details.get('conditions', 'Aucune condition disponible.')}")
                    st.markdown(f"**⚔️ Arme :** {item_details.get('is_weapon', 'Non')}")
                    st.markdown(f"**🎯 Critique :** {item_details.get('critical_hit_probability', 'N/A')}%")

            else:
                st.warning("❗ L'item est incomplet, données brutes :")
                st.json(item)
