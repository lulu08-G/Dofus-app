import streamlit as st
import requests

st.set_page_config(page_title="🔍 Recherche Items Dofus", layout="centered")
st.title("🔍 Recherche d'équipements Dofus")

# Fonction de recherche d'items
def search_items(query):
    if not query:
        return []
    
    params = {
        "query": query,
        "limit": 10
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        items = response.json()
        
        # On filtre uniquement les équipements côté Python
        equipment_items = [
            item for item in items if item['item_subtype']['name_id'] == "equipment"
        ]
        
        return equipment_items
    else:
        st.error(f"Erreur API : {response.status_code}")
        return []

# Fonction pour afficher les détails d'un item
def show_item_details(item):
    st.header(f"{item.get('name')} (Niveau {item.get('level')})")
    st.image(item['image_urls']['icon'], width=150)

    st.markdown("### Informations principales")
    st.markdown(f"**ID Ankama** : {item.get('ankama_id')}")
    st.markdown(f"**Type** : {item['type'].get('name')}")
    st.markdown(f"**Sous-Type** : {item['item_subtype'].get('name_id')}")

    st.markdown("### Description")
    st.info(item.get('description', "Pas de description disponible."))

    # Afficher les prix si disponibles
    prices = item.get('prices')
    if prices:
        st.markdown("### Prix (HDV)")
        for key, value in prices.items():
            st.write(f"{key} : {value}")
    else:
        st.warning("Pas d'informations de prix disponibles.")

# Input de recherche
search_query = st.text_input("Tape le nom de l'équipement recherché :", "")

# Résultats de recherche
if search_query:
    items = search_items(search_query)

    if items:
        st.subheader("Résultats de recherche :")

        # Liste cliquable des items
        for item in items:
            if st.button(f"{item.get('name')} (Lvl {item.get('level')})", key=item.get('ankama_id')):
                show_item_details(item)
    else:
        st.warning("Aucun équipement trouvé pour cette recherche.")
