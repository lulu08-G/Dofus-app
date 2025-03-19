import streamlit as st
import requests
import json

# Configuration du thème sombre
st.set_page_config(page_title="🔨 Craft Dofus 🔨", page_icon="⚒️", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #f5f5f5;
        }
        .css-1v3fvcr {
            background-color: #212121;
        }
        .css-1gkfh0p {
            background-color: #333333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stMarkdown {
            color: #f5f5f5;
        }
        .stExpanderHeader {
            color: #f5f5f5;
        }
        .stTable th {
            background-color: #2e2e2e;
        }
        .stTable td {
            background-color: #333333;
            color: #f5f5f5;
        }
    </style>
    """, unsafe_allow_html=True
)

# Titre de la page
st.title("🔨 Craft Dofus 🔨")

# Recherche d'un item
search_query = st.text_input("Recherche d'un équipement :", "")

# Fonction pour rechercher des items
def search_items(query):
    if not query:
        return []

    params = {
        "query": query,
        "limit": 5
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            return response.json()  # La réponse est directement une liste d'items
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            st.text(response.text)  # Afficher la réponse brute pour déboguer
            return []
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

# Fonction pour obtenir les détails de l'item
def get_item_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/equipment/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # La réponse est un dictionnaire contenant les détails de l'item
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            st.text(response.text)  # Afficher la réponse brute pour déboguer
            return {}
    else:
        st.error(f"Erreur API : {response.status_code}")
        return {}

# Fonction pour afficher la recette
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

# Fonction pour afficher les statistiques de l'item
def show_item_stats(item):
    # Affichage des statistiques de l'item
    stats = item.get('effects', [])

    if not stats:
        st.warning("Aucune statistique disponible pour cet item.")
        return

    data = []
    for stat in stats:
        stat_type = stat['type']['name']
        min_value = stat.get('int_minimum', 'N/A')
        max_value = stat.get('int_maximum', 'N/A')
        formatted = stat.get('formatted', 'N/A')

        data.append([stat_type, min_value, max_value, formatted])

    # Tableau des statistiques
    st.markdown("### 📊 Statistiques :")
    if data:
        st.table(data)

# Si une recherche est faite :
if search_query:
    items = search_items(search_query)

    if not items:
        st.warning("Aucun résultat trouvé pour cette recherche.")
    else:
        st.subheader("📋 Résultats :")
        
        for item in items:
            # Vérifier si l'item contient bien un nom et un niveau
            if 'name' in item and 'level' in item:
                with st.expander(f"{item['name']} (Lvl {item['level']})"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        st.image(item['image_urls']['icon'], width=80)

                    with col2:
                        st.markdown(f"**Nom :** {item['name']}")
                        st.markdown(f"**Niveau :** {item['level']}")
                        st.markdown(f"**Type :** {item['type']['name']}")
                        st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")

                    # Récupérer les détails supplémentaires de l'item
                    item_details = get_item_details(item['ankama_id'])

                    # Afficher la recette si elle existe
                    if 'recipe' in item_details and item_details['recipe']:
                        st.markdown("---")
                        st.markdown("### 🧪 Recette de craft :")
                        show_recipe(item_details['recipe'])
                    else:
                        st.info("Pas de recette disponible pour cet item.")
                
                    # Afficher les statistiques
                    show_item_stats(item_details)

                    # Autres informations à afficher
                    st.markdown("### Informations supplémentaires :")
                    st.markdown(f"**Pods :** {item_details.get('pods', 'N/A')}")
                    st.markdown(f"**Conditions :** {item_details.get('conditions', 'Aucune condition disponible.')}")

            else:
                st.warning(f"L'item ne contient pas les informations attendues (manque 'name' ou 'level'). Voici les données complètes :")
                st.json(item)

