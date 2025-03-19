import streamlit as st
import requests
import json

# Fonction pour rechercher une ressource via l'ankama_id
def get_resource_details(ankama_id):
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # Retourne les détails de la ressource
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            st.text(response.text)  # Afficher la réponse brute pour déboguer
            return {}
    else:
        st.error(f"Erreur API : {response.status_code}")
        return {}

# Fonction pour afficher la recette avec les ressources détaillées
def show_recipe(recipe):
    if not recipe:
        st.warning("❌ Pas de recette pour cet item.")
        return

    st.success("✅ Recette disponible !")

    for ingredient in recipe:
        item_id = ingredient['item_ankama_id']
        quantity = ingredient['quantity']
        subtype = ingredient['item_subtype']

        # Recherche de la ressource avec l'ankama_id (ici, l'item_id)
        resource_details = get_resource_details(item_id)

        if resource_details:
            resource_name = resource_details.get('name', 'Inconnu')
            resource_image = resource_details.get('image_urls', {}).get('icon', None)

            # Affichage de la recette avec l'image et le nom de la ressource
            col1, col2 = st.columns([1, 3])
            with col1:
                if resource_image:
                    st.image(resource_image, width=80)
                else:
                    st.image("https://via.placeholder.com/80", width=80)  # Image de remplacement si aucune image

            with col2:
                st.markdown(f"➡️ **{quantity}x** **{resource_name}** (ID : `{item_id}`) - Type : {subtype}")

# Exemple d'utilisation dans ton code principal
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
                        st.image(item['image_urls']['icon'], width=120)  # Image plus grande

                    with col2:
                        # Style amélioré avec des titres plus visibles et une structure claire
                        st.markdown(f"**Nom :** {item['name']}")
                        st.markdown(f"**Niveau :** {item['level']}")
                        st.markdown(f"**Type :** {item['type']['name']}")
                        st.markdown(f"**Description :** {item.get('description', 'Aucune description disponible.')}")

                    item_details = get_item_details(item['ankama_id'])

                    # Affichage de la recette
                    if 'recipe' in item_details and item_details['recipe']:
                        st.markdown("---")
                        st.markdown("### 🧪 Recette de craft :")
                        show_recipe(item_details['recipe'])
                    else:
                        st.info("Pas de recette disponible pour cet item.")

                    # Affichage des statistiques
                    show_item_stats(item_details)

                    # Informations supplémentaires
                    st.markdown("### Informations supplémentaires :")
                    st.markdown(f"**Pods :** {item_details.get('pods', 'N/A')}")
                    st.markdown(f"**Conditions :** {item_details.get('conditions', 'Aucune condition disponible.')}")

