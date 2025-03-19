import streamlit as st
import requests

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

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/all"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
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

        # Afficher les détails de chaque ingrédient
        st.markdown(f"➡️ **{quantity}x** [Item ID : `{item_id}`] - Type : {subtype}")
        
        # Optionnel: Ajouter plus d'infos sur chaque ingrédient

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
            # Vérification des données de l'item avant d'y accéder
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
            else:
                st.warning(f"L'item {item} semble manquer d'une clé 'name' ou 'level'.")

