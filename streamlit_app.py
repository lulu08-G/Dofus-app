import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

def search_items(query):
    if not query:
        st.warning("Tape un nom d'objet !")
        return []
    
    params = {
        "query": query,
        "limit": 5
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/search"
    response = requests.get(url, params=params)

    # Debug : voir ce que l'API répond
    st.write("Status code:", response.status_code)
    st.write("Response text:", response.text)

    if response.status_code == 200:
        data = response.json()
        return data.get("data", [])
    else:
        st.error("Erreur API : " + str(response.status_code))
        return []

if search_query:
    items = search_items(search_query)
    for item in items:
        st.image(item['img'], width=100)
        st.subheader(item['name'])
        st.write(f"Niveau : {item['level']}")
