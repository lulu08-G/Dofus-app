def get_item_details(ankama_id):
    # URL mise à jour : recherche dans les ressources
    url = f"https://api.dofusdu.de/dofus3/v1/fr/items/resources/{ankama_id}"
    response = requests.get(url)

    if response.status_code == 200:
        try:
            return response.json()  # La réponse est un dictionnaire contenant les détails de la ressource
        except json.JSONDecodeError:
            st.error("Erreur de formatage JSON : la réponse de l'API n'est pas un JSON valide.")
            st.text(response.text)
            return {}
    else:
        st.error(f"Erreur API : {response.status_code}")
        return {}
