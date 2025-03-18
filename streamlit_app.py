import streamlit as st
import requests

st.title("🔨 Craft Dofus 🔨")

search_query = st.text_input("Recherche d'un item :", "")

def search_items(query):
    if not query:
        return []
    
    params = {
        "query": query,
        "limit": 5
    }

    url = "https://api.dofusdu.de/dofus3/v1/fr/items/search"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return []

def get_recipe(item_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/recipes/{item_id}"
    response = requests.get(url)

    st.write("Recipe API response:", response.status_code, response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return None

if search_query:
    items = search_items(search_query)

    st.subheader("📝 Résultats de recherche")
    for item in items:
        with st.expander(f"{item['name']} (Lvl {item['level']})"):
            st.image(item['image_urls']['icon'], width=100)

            if st.button(f"Voir la recette de {item['name']}", key=item['ankama_id']):
                recipe = get_recipe(item['ankama_id'])

                if recipe and "ingredients" in recipe.get('result', {}):
                    st.success(f"Recette pour {item['name']}")

                    for ingredient in recipe['result']['ingredients']:
                        ingr = ingredient['item']
                        qty = ingredient['quantity']

                        st.markdown(f"### {qty} x {ingr['name']}")
                        st.image(ingr['image_urls']['icon'], width=80)
                else:
                    st.warning("Pas de recette disponible pour cet item !")
