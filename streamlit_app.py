import streamlit as st
import requests
import json
import subprocess

# Initialise Doduda (le client DofusDB)
doduda = Doduda()


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
    # CSS personnalisé
    css = """
    <style>
        :root {
            --font-main: "Lato", Arial, sans-serif;
            --font-bold: "Lato Bold", Arial, sans-serif;
            --font-size-xl: 1.5rem;
            --font-size-l: 1.2rem;
            --font-size-m: 1rem;
            --font-size-s: 0.875rem;
            --color-primary: #4a433b;
            --color-secondary: #6aa84f;
            --color-light: #f8f9fa;
            --color-dark: #212529;
            --color-text: #495057;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--color-light);
            color: var(--color-text);
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        header {
            background-color: var(--color-primary);
            color: white;
            padding: 1rem;
            text-align: center;
            font-size: var(--font-size-xl);
        }

        nav {
            background-color: var(--color-secondary);
            padding: 0.75rem;
            display: flex;
            justify-content: center;
        }

        nav a {
            text-decoration: none;
            color: white;
            font-size: var(--font-size-m);
            padding: 0.5rem 1rem;
            transition: background-color 0.3s;
        }

        nav a:hover {
            background-color: var(--color-primary);
        }

        .main-content {
            padding: 2rem;
        }

        .card {
            background-color: var(--color-light);
            border: 1px solid #e0e0e0;
            padding: 1rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }

        .card:hover {
            transform: scale(1.05);
        }

        footer {
            background-color: var(--color-primary);
            color: white;
            text-align: center;
            padding: 1rem;
            position: fixed;
            width: 100%;
            bottom: 0;
        }
    </style>
    """

    # HTML de la page
    html = """
    <header>
        <h1>Bienvenue sur ma page</h1>
    </header>

    <nav>
        <a href="#">Accueil</a>
        <a href="#">À propos</a>
        <a href="#">Services</a>
        <a href="#">Contact</a>
    </nav>

    <div class="main-content">
        <div class="card">
            <h2>Card 1</h2>
            <p>Ceci est un exemple de carte avec un peu de contenu pour montrer l'effet d'ombre et de survol.</p>
        </div>

        <div class="card">
            <h2>Card 2</h2>
            <p>Une autre carte, toujours avec un effet de survol qui l'agrandit légèrement.</p>
        </div>

        <div class="card">
            <h2>Card 3</h2>
            <p>Encore une carte, avec un texte explicatif pour tester l'espacement et la mise en page.</p>
        </div>
    </div>

    <footer>
        <p>&copy; 2025 Ma page avec style CSS personnalisé</p>
    </footer>
    """

    # Injection CSS et HTML dans Streamlit
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)

# ========================
# Douda
# ========================
elif page == "dou":
        # Titre de l'application
    st.title("🔎 Dofus Drop Finder")
    
    # Champ de recherche utilisateur
    search_query = st.text_input("Recherche un monstre 🐲 :", "")
    
    # Si l'utilisateur tape quelque chose
    if search_query:
        # Recherche le monstre dans Doduda
        monsters = doduda.search('monsters', search_query)
    
        if monsters:
            # Affiche chaque monstre trouvé
            for monster in monsters:
                st.header(monster['name']['fr'])
    
                # Niveau du monstre
                st.subheader(f"Niveau : {monster.get('level', 'Inconnu')}")
    
                # Liste des drops du monstre
                drops = monster.get('drops', [])
    
                if drops:
                    st.write("💎 **Drops :**")
                    for drop in drops:
                        item_name = drop['item']['name']['fr']
                        drop_rate = drop.get('percentDropForProspecting', 0)
                        st.write(f"- **{item_name}** : {drop_rate}% de chance avec 100PP")
                else:
                    st.info("Aucun drop trouvé pour ce monstre 😢")
        else:
            st.warning("Aucun monstre trouvé avec ce nom.")
    else:
        st.info("Tape le nom d'un monstre pour commencer la recherche !")
    
    # Footer
    st.markdown("---")
    st.caption("⚔️ App créée avec Doduda + Streamlit by ChatGPT 😉")
