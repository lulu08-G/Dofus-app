import streamlit as st
from dofapi import DofusAPI

# Initialise l'API
api = DofusAPI()

st.title("🔎 Encyclopédie Dofus (via dofapi)")

search_query = st.text_input("Recherche d'un item :", "")

# Si on tape quelque chose
if search_query:
    # On cherche des items par le nom
    items = api.items.search(query=search_query, lang='fr')

    # Vérif si on trouve quelque chose
    if not items:
        st.warning("Aucun item trouvé !")
    else:
        # Boucle sur chaque item trouvé
        for item in items:
            st.subheader(f"{item['name']} (Lvl {item['level']})")
            st.image(item['image_urls']['icon'], width=100)

            # Affiche les infos de base
            st.markdown(f"**ID** : {item['ankama_id']}")
            st.markdown(f"**Type** : {item['type']['name']}")
            st.markdown(f"**Niveau** : {item['level']}")
            st.markdown(f"**Sous-type** : {item['item_subtype']['name_id']}")
            st.markdown(f"**Lien vers l'image HD** : {item['image_urls']['sd']}")
            
            # Tu peux afficher plus d'infos si dispo
            st.json(item)  # Affiche tout l'objet brut

            # TODO : Si la lib expose la recette, on pourrait ajouter ici
            # ex: recipe = api.recipes.get_by_item_id(item['ankama_id'])
