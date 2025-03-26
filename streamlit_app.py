import streamlit as st
import requests
import json
import subprocess
import os 
import io
import zipfile



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
    st.title("Page DESIGNE")

    def download_and_extract_artifact():
        # Lien vers l'artefact GitHub
        artifact_url = "https://api.github.com/repos/lulu08-G/Dofus-app/actions/artifacts/2814294485/zip"
        GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"] if "GITHUB_TOKEN" in st.secrets else None
        
        if not GITHUB_TOKEN:
            st.error("❌ Erreur : Token GitHub manquant.")
            return
        
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
    
        zip_path = "artifact.zip"
        max_file_size = 3000 * 1024 * 1024  # 1000 MB (3 Go)
    
        # 🎯 Vérification de la taille du fichier avant le téléchargement
        st.write("🔄 Vérification de la taille du fichier...")
    
        try:
            # Récupérer la taille du fichier via l'API GitHub
            response = requests.head(artifact_url, headers=headers, allow_redirects=True)
            if response.status_code == 200:
                file_size = int(response.headers.get('Content-Length', 0))
                st.write(f"📏 Taille du fichier : {file_size / (1024 * 1024):.2f} MB")
                
                if file_size > max_file_size:
                    st.error(f"❌ Le fichier est trop gros ({file_size / (1024 * 1024):.2f} MB). Taille maximale autorisée : {max_file_size / (1024 * 1024):.2f} MB.")
                    return
            else:
                st.error(f"❌ Erreur lors de la récupération des informations sur le fichier : {response.status_code}")
                return
        except Exception as e:
            st.error(f"❌ Erreur lors de la vérification de la taille : {e}")
            return
    
        # 🎯 Démarrer le téléchargement
        st.write("🔄 Téléchargement du fichier...")
    
        try:
            with requests.get(artifact_url, headers=headers, stream=True, timeout=300) as response:
                if response.status_code == 200:
                    with open(zip_path, "wb") as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    st.success(f"✅ Fichier téléchargé : {zip_path}")
                    
                    # 🎯 Décompresser l'archive
                    st.write("✅ Décompression du fichier ZIP...")
    
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall("resultats")  # Extraire dans le dossier 'resultats'
                    st.write("✅ Artefact extrait avec succès.")
                    
                    # Lister les fichiers extraits
                    files = os.listdir("resultats")
                    st.write("📂 Contenu du dossier 'resultats' :", files)
                else:
                    st.error(f"❌ Erreur lors du téléchargement : {response.status_code}")
                    st.write(response.text)  # Afficher la réponse de GitHub pour le débogage
        except requests.exceptions.Timeout:
            st.error("❌ Timeout pendant le téléchargement. L'opération a pris trop de temps.")
        except Exception as e:
            st.error(f"❌ Erreur pendant le téléchargement ou la décompression : {e}")

    download_and_extract_artifact()

    
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
