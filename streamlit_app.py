import streamlit as st
import requests
import json

# ========================
# MENU DE NAVIGATION
# ========================
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio("Aller à :", ["Accueil", "Test Image Item", "Page test", "DESIGNE"])

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
# DESIGNE
# ========================
elif page == "DESIGNE":


    st.title("🧑‍🎓 DofusBook - Equipement & Statistiques 🛡️")
    
    # Exemple d'équipement
    st.subheader("🔨 Nom de l'équipement : Epée de Légende")
    
    # Image de l'équipement
    st.image("https://via.placeholder.com/150", width=150)
    
    # Informations principales
    st.markdown("**Niveau :** 100")
    st.markdown("**Type :** Epée")
    st.markdown("**Description :** Une épée légendaire forgée dans les flammes d'un volcan.")
    st.markdown("**Pods :** 10")
    st.markdown("**Critiques :** 10% de chance de coup critique")
    
    # Section des statistiques de l'équipement
    st.subheader("📊 Statistiques de l'équipement")
    
    # Tableau des statistiques
    stats_data = [
        ["Attaque", 50, 100, "50 à 100"],
        ["Chance", 10, 20, "10 à 20"],
        ["Agilité", 15, 30, "15 à 30"],
        ["Vitalité", 100, 150, "100 à 150"]
    ]
    
    st.table(stats_data)
    
    # Section de la recette de craft
    st.subheader("🧪 Recette de Craft")
    
    recipe_data = [
        ["Ingrédient 1", 3, "Item 1"],
        ["Ingrédient 2", 2, "Item 2"],
        ["Ingrédient 3", 5, "Item 3"]
    ]
    
    # Affichage des ingrédients nécessaires à la recette
    st.markdown("**Pour crafter cette épée, vous aurez besoin de :**")
    
    for ingredient in recipe_data:
        st.markdown(f"➡️ **{ingredient[1]}x** {ingredient[0]} (Type : {ingredient[2]})")
    
    # Informations supplémentaires
    st.subheader("💡 Informations supplémentaires")
    
    st.markdown("**Conditions d'utilisation :**")
    st.markdown("- Niveau 100 requis.")
    st.markdown("- Doit être utilisé par un guerrier de la lumière.")
    
    # Footer pour un style visuel
    st.markdown("---")
    st.markdown("**DofusBook - Simulation d'équipement**")
