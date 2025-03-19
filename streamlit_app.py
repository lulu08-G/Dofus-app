import streamlit as st
import requests
import json

st.title("🔨 Recherche d'Equipement Dofus 🔨")

# Recherche d'un item
search_query = st.text_input("Entrez le nom d'un équipement à rechercher :", "")

# Nombre d'items à afficher par recherche
LIMIT = 10
PAGE = 1

def search_items(query, page=1):
    if not query:
        return []

    params = {
        "query": query,  # Mot-clé de recherche
        "limit": LIMIT,   # Limiter le nombre d'items renvoyés
        "page": page      # Pagination : numéro de la page
    }

    # Utilisation de l'endpoint /search pour la recherche d'items
    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            response_data = response.json()
            if 'items' in response_data:
                return response_data['items']
            else:
                st.error("Aucun item trouvé dans la réponse de l'API.")
                return []
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            return []
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.success("✅ Recette disponible !")
    for ingredient in recipe:
        item_id = ingredient['item_ankama_id']
        quantity = ingredient['quantity']
        subtype = ingredient['item_subtype']
        # Afficher l'ingredient avec son image
        st.markdown(f"➡️ **{quantity}x** [Item ID : `{item_id}`] - Type : {subtype}")
        
        # Ajouter un lien ou une image pour chaque ingrédient
        item_url = f"https://api.dofusdu.de/dofus3/v1/img/item/{item_id}-64.png"
        st.image(item_url, width=50)

def show_item_stats(item):
    st.subheader(f"📊 Statistiques de {item['name']}")
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
    if data:
        st.table(data)

def display_pagination(page):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if page > 1:
            prev_page = page - 1
            if st.button(f"Page {prev_page}"):
                return prev_page
    with col2:
        st.markdown(f"**Page {page}**")
    with col3:
        next_page = page + 1
        if st.button(f"Page {next_page}"):
            return next_page
    return page

# Si une recherche est faite :
if search_query:
    items = search_items(search_query, page=PAGE)

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
                        st.image(item['image_urls']['icon'], width=100)

                    with col2:
                        st.markdown(f"**Nom :** {item['name']}")
                        st.markdown(f"**Niveau :** {item['level']}")
                        st.markdown(f"**Type :** {item['type']['name']}")
                        st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")

                    # Afficher la recette si elle existe
                    if 'recipe' in item and item['recipe']:
                        st.markdown("---")
                        st.markdown("### 🧪 Recette de craft :")
                        show_recipe(item['recipe'])
                    else:
                        st.info("Pas de recette disponible pour cet item.")
                
                    # Afficher les statistiques
                    show_item_stats(item)

                    # Autres informations à afficher
                    st.markdown("### Informations supplémentaires :")
                    st.markdown(f"**Pods :** {item.get('pods', 'N/A')}")
                    st.markdown(f"**Conditions :** {item.get('conditions', 'Aucune condition disponible.')}")
                    st.markdown(f"**Equipement :** {item.get('is_weapon', 'N/A')}")
                    st.markdown(f"**Critiques :** Probabilité critique: {item.get('critical_hit_probability', 'N/A')}%")

        # Pagination
        PAGE = display_pagination(PAGE)

