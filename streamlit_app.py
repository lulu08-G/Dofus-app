import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

def search_items(query):
    params = {"query": query, "limit": 5}
    response = requests.get("https://api.dofusdu.de/dofus3/v1/fr/items/search", params=params)
    if response.status_code == 200:
        return response.json()["data"]
    return []

if search_query:
    items = search_items(search_query)
    for item in items:
        st.image(item['img'], width=100)
        st.subheader(item['name'])
        st.write(f"Niveau : {item['level']}")