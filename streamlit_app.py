import streamlit as st
import requests
import json

st.title("🔨 Craft Dofus 🔨")

# Recherche d'un item
search_query = st.text_input("Recherche d'un équipement :", "")

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

def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.success("✅ Recette disponible !")

    # Pour chaque ingrédient de la recette
    for ingredient in recipe:
        item_id = ingredient['item_ankama_id']  # On récupère l'ID de l'item
        quantity = ingredient['quantity']  # Quantité d'ingrédient
        subtype = ingredient['item_subtype']  # Type d'ingrédient (facultatif, à afficher si besoin)

        # Utilisation de get_item_details pour récupérer les détails de l'item
       def get_item_details(ankama_id):
    # Remplacer 'equipment' par 'resources' dans l'URL
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # Retourne les détails de l'item
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            st.text(response.text)  # Afficher la réponse brute pour déboguer
            return {}
    else:
        st.error(f"Erreur API : {response.status_code}")
        return {}



        # Si on a bien récupéré les détails de l'item
        if item_details:
            # On suppose que l'item a une clé 'name' et 'image_urls'
            item_name = item_details.get('name', 'Nom non trouvé')
            item_image_url = item_details.get('image_urls', {}).get('icon', '')  # Image de l'item

            # Affichage de la recette : quantité, x, image de la ressource et nom de la ressource
            col1, col2 = st.columns([1, 3])

            with col1:
                if item_image_url:  # Si on a une URL d'image valide
                    st.image(item_image_url, width=50)  # Afficher l'image de l'item

            with col2:
                st.markdown(f"➡️ **{quantity}x** - {item_name}")

def show_item_stats(item):
    # Affichage des statistiques de l'item
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
                    st.markdown(f"**Equipement :** {item_details.get('is_weapon', 'N/A')}")
                    st.markdown(f"**Critiques :** Probabilité critique : {item_details.get('critical_hit_probability', 'N/A')}%")
            else:
                st.warning(f"L'item ne contient pas les informations attendues (manque 'name' ou 'level'). Voici les données complètes :")
                st.json(item)
