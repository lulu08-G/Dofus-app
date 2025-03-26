import streamlit as st
import requests
import json
import subprocess
import os 
import io
import zipfile
import pandas as pd


# Configuration de la page doit être la première commande Streamlit
st.set_page_config(
    page_title="Page avec CSS personnalisé",
    page_icon="✨",
    layout="wide"
)

# ========================
# MENU DE NAVIGATION
# ========================
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Aller à :", ["Accueil", "Test Image Item", "Page test", "DESIGNE", "dou"])

# ========================
# PAGE ACCUEIL
# ========================
if page == "Accueil":
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
                return response.json()
            except json.JSONDecodeError:
                st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
                st.text(response.text)
                return {}
        else:
            st.error(f"Erreur API : {response.status_code}")
            return {}

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

        if data:
            st.table(data)

    if search_query:
        items = search_items(search_query)

        if not items:
            st.warning("Aucun résultat trouvé pour cette recherche.")
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
                            st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")

                        item_details = get_item_details(item['ankama_id'])

                        if 'recipe' in item_details and item_details['recipe']:
                            st.markdown("---")
                            st.markdown("### 🧪 Recette de craft :")
                            show_recipe(item_details['recipe'])
                        else:
                            st.info("Pas de recette disponible pour cet item.")

                        show_item_stats(item_details)

                        st.markdown("### Informations supplémentaires :")
                        st.markdown(f"**Pods :** {item_details.get('pods', 'N/A')}")
                        st.markdown(f"**Conditions :** {item_details.get('conditions', 'Aucune condition disponible.')}")
                        st.markdown(f"**Equipement :** {item_details.get('is_weapon', 'N/A')}")
                        st.markdown(f"**Critiques :** Probabilité critique : {item_details.get('critical_hit_probability', 'N/A')}%")

                else:
                    st.warning("Item incomplet :")
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



# ========================
# PAGE TEST
# ========================
elif page == "Page test":
    st.title("🧪 Test Affichage Image Item")

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
                return response.json()
            except json.JSONDecodeError:
                st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
                st.text(response.text)
                return {}
        else:
            st.error(f"Erreur API : {response.status_code}")
            return {}

    def get_resource_details(item_id):  # Correction de l'argument ici : 'ankama_id' -> 'item_id'
        url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{item_id}"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
                st.text(response.text)
                return {}
        else:
            st.error(f"Erreur API : {response.status_code}")
            return {}

    def show_recipe(recipe):
        if not recipe:
            st.warning("❌ Pas de recette pour cet item.")
            return

        st.success("✅ Recette disponible !")

        # ✅ Vérification pour éviter NameError
        if not isinstance(recipe, list):
            st.error("⚠️ Erreur : la recette n'est pas une liste valide.")
            st.write(recipe)  # Debugging
            return

        for ingredient in recipe:
            item_id = ingredient.get('item_ankama_id')
            quantity = ingredient.get('quantity')
            subtype = ingredient.get('item_subtype')

            # 🔎 Récupérer les détails de la ressource
            item_details = get_resource_details(item_id)  # Utilisation de get_resource_details avec item_id

            if not item_details:
                st.warning(f"❗ Détails introuvables pour l'ID {item_id}")
                continue

            item_name = item_details.get('name', 'Nom inconnu')
            image_url = item_details.get('image_urls', {}).get('icon')

            # 🖼️ Affichage en colonnes
            cols = st.columns([1, 5])

            with cols[0]:
                if image_url:
                    st.image(image_url, width=20, use_container_width=True)
                else:
                    st.write("❓")  # Icône manquante

            with cols[1]:
                st.markdown(f"**{quantity}x** {item_name} _(Type : {subtype})_")

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

        if data:
            st.table(data)

    if search_query:
        items = search_items(search_query)

        if not items:
            st.warning("Aucun résultat trouvé pour cette recherche.")
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
                            st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")

                        # **PROBLÈME DE L'INDENTATION** :
                        # Ligne suivante maintenant correctement indentée
                        item_details = get_item_details(item['ankama_id'])

                        if 'recipe' in item_details and item_details['recipe']:
                            st.markdown("---")
                            st.markdown("### 🧪 Recette de craft :")
                            show_recipe(item_details['recipe'])
                        else:
                            st.info("Pas de recette disponible pour cet item.")

                        show_item_stats(item_details)

                        st.markdown("### Informations supplémentaires :")
                        st.markdown(f"**Pods :** {item_details.get('pods', 'N/A')}")
                        st.markdown(f"**Conditions :** {item_details.get('conditions', 'Aucune condition disponible.')}") 
                        st.markdown(f"**Equipement :** {item_details.get('is_weapon', 'N/A')}")
                        st.markdown(f"**Critiques :** Probabilité critique : {item_details.get('critical_hit_probability', 'N/A')}%")

                else:
                    st.warning("Item incomplet :")
                    st.json(item)





# ========================
# PAGE DESIGNE
# ========================
elif page == "DESIGNE":
    def load_json_files(directory):
        files = {}
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                files[filename] = data
        return files
    
    # Fonction pour afficher les résultats de manière paginée
    def display_paginated_data(data, page_size=10, page_num=1):
        start = (page_num - 1) * page_size
        end = start + page_size
        data_paginated = data[start:end]
        
        for idx, item in enumerate(data_paginated, start=start + 1):
            st.write(f"**{idx}**: {item}")
        
        return len(data_paginated)
    
    # Fonction pour rechercher dans les fichiers
    def search_in_files(files, query):
        results = {}
        for file_name, data in files.items():
            if isinstance(data, list):  # Si les données sont une liste (souvent le cas avec les fichiers JSON)
                results[file_name] = [item for item in data if query.lower() in str(item).lower()]
            elif isinstance(data, dict):  # Si les données sont un dictionnaire
                results[file_name] = [item for item in data.items() if query.lower() in str(item).lower()]
        return results
    
    # Fonction principale pour l'interface Streamlit
    def main():
        st.title("📚 Navigateur de fichiers JSON")
        st.write("Explorez les fichiers JSON extraits et recherchez des informations.")
    
        # Charger les fichiers JSON
        directory = "resultats"  # Chemin vers le dossier contenant les fichiers JSON
        files = load_json_files(directory)
    
        # Barre de recherche
        query = st.text_input("🔍 Recherchez dans les fichiers JSON :", "")
        
        # Afficher les résultats de la recherche si une requête est donnée
        if query:
            st.subheader(f"Résultats pour '{query}' :")
            search_results = search_in_files(files, query)
            
            if not any(search_results.values()):
                st.write("❌ Aucune donnée correspondante trouvée.")
            else:
                for file_name, results in search_results.items():
                    if results:
                        st.write(f"**{file_name}**:")
                        display_paginated_data(results, page_size=5, page_num=1)  # Affichage paginé
    
        # Sélectionner un fichier pour afficher son contenu
        selected_file = st.selectbox("📁 Sélectionnez un fichier JSON à afficher :", list(files.keys()))
        
        # Si un fichier est sélectionné, afficher son contenu
        if selected_file:
            st.subheader(f"Contenu de {selected_file}:")
            data = files[selected_file]
    
            # Si c'est une liste, on peut l'afficher sous forme de table
            if isinstance(data, list):
                df = pd.DataFrame(data)
                st.dataframe(df)
            elif isinstance(data, dict):  # Si c'est un dictionnaire
                st.write(json.dumps(data, indent=2))
    
        # Paginée : Si les données sont volumineuses
        st.write("### Pages de résultats :")
        if st.button('Afficher les pages suivantes'):
            # Recharger ou mettre à jour la pagination
            display_paginated_data(data, page_size=5, page_num=2)
    
    if __name__ == "__main__":
        main()
    
# ========================
# Douda
# ========================
elif page == "dou":
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            st.write(f'{indent}{os.path.basename(root)}/')
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                st.write(f'{subindent}{f}')
    
    # Chemin de départ à partir duquel lister les fichiers (par exemple, le répertoire actuel)
    startpath = '.'
    
    st.title("Arborescence des fichiers")
    list_files(startpath)
