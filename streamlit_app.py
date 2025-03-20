import streamlit as st
import requests
import json

st.title("🔨 Craft Dofus 🔨")

# ------------------ RECHERCHE ITEM PRINCIPAL ------------------

search_query = st.text_input("Recherche d'un équipement :", "")

def search_items(query):
    if not query:
        return []
    params = { "query": query, "limit": 5 }
    url = "https://api.dofusdu.de/dofus3/v1/fr/items/equipment/search"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("Erreur JSON (items search).")
            st.text(response.text)
            return []
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

@st.cache_data
def get_item_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/equipment/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("Erreur JSON (item details).")
            st.text(response.text)
            return {}
    else:
        st.error(f"Erreur API : {response.status_code}")
        return {}

@st.cache_data
def get_resource_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error(f"Erreur JSON pour l'ID {ankama_id}")
            return {}
    else:
        st.error(f"Erreur API {response.status_code} pour l'ID {ankama_id}")
        return {}

def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.success("✅ Recette disponible !")

    for ingredient in recipe:
        item_id = ingredient.get('item_ankama_id')
        quantity = ingredient.get('quantity')

        if item_id is None or quantity is None:
            st.warning("❗ Ingredient incomplet.")
            continue

        # Détails de l'ingrédient
        resource_details = get_resource_details(item_id)

        if resource_details:
            item_name = resource_details.get('name', 'Nom inconnu')
            item_image = resource_details.get('image_urls', {}).get('icon', None)

            cols = st.columns([1, 6])

            with cols[0]:
                if item_image:
                    st.image(item_image, width=40)
                else:
                    st.write("❓")

            with cols[1]:
                st.markdown(f"**{quantity}x {item_name}**")
        else:
            st.warning(f"Détails introuvables pour l'ID {item_id}")

def show_item_stats(item):
    st.subheader(f"📊 Statistiques de {item['name']}")
    stats = item.get('effects', [])

    if not stats:
        st.warning("Aucune statistique disponible.")
        return

    data = []
    for stat in stats:
        stat_type = stat['type']['name']
        min_value = stat.get('int_minimum', 'N/A')
        max_value = stat.get('int_maximum', 'N/A')
        formatted = stat.get('formatted', 'N/A')

        data.append([stat_type, min_value, max_value, formatted])

    st.table(data)

# ------------------ AFFICHAGE PRINCIPAL ------------------

if search_query:
    items = search_items(search_query)

    if not items:
        st.warning("Aucun résultat trouvé.")
    else:
        st.subheader("📋 Résultats :")

        for item in items:
            if 'name' in item and 'level' in item:
                with st.expander(f"{item['name']} (Lvl {item['level']})"):
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        st.image(item['image_urls']['icon'], width=80)

                    with col2:
                        st.markdown(f"**Nom :** {item['name']}")
                        st.markdown(f"**Niveau :** {item['level']}")
                        st.markdown(f"**Type :** {item['type']['name']}")
                        st.markdown(f"**Description :** {item.get('description', 'Aucune description.')}")

                    # Détails de l'item complet
                    item_details = get_item_details(item['ankama_id'])

                    # Afficher la recette si disponible
                    if 'recipe' in item_details and item_details['recipe']:
                        st.markdown("---")
                        st.markdown("### 🧪 Recette de craft :")
                        show_recipe(item_details['recipe'])
                    else:
                        st.info("Pas de recette disponible.")

                    # Stats
                    show_item_stats(item_details)

                    # Autres infos
                    st.markdown("### Informations supplémentaires :")
                    st.markdown(f"**Pods :** {item_details.get('pods', 'N/A')}")
                    st.markdown(f"**Conditions :** {item_details.get('conditions', 'Aucune condition.')}")
                    st.markdown(f"**Equipement :** {item_details.get('is_weapon', 'N/A')}")
                    st.markdown(f"**Critiques :** {item_details.get('critical_hit_probability', 'N/A')}%")
            else:
                st.warning("Item incomplet (pas de name ou de level)")
                st.json(item)


# ========================
# PAGE TEST IMAGE ITEM
# ========================
elif page == "Test Image Item":
    st.title("🧪 Test Affichage Image Item")

    ankama_id = st.text_input("Entrez l'ID Ankama de l'item :", "")

    def get_resource_details(ankama_id):
        url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                st.error("Erreur JSON : réponse de l'API invalide.")
                st.text(response.text)
                return {}
        else:
            st.error(f"Erreur API : {response.status_code}")
            return {}

    if ankama_id:
        item_details = get_resource_details(ankama_id)

        if item_details:
            st.markdown(f"### Résultat pour l'ID Ankama `{ankama_id}`")

            image_url = item_details.get('image_urls', {}).get('icon', None)
            item_name = item_details.get('name', 'Nom inconnu')

            st.markdown(f"**Nom :** {item_name}")

            if image_url:
                st.image(image_url, width=150)
            else:
                st.warning("Aucune image trouvée pour cet item.")
        else:
            st.warning("Aucun détail trouvé pour cet ID Ankama.")
