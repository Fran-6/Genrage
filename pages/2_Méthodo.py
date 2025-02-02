import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )


md= """
### Genrage

##### Classificateur de genre : Utilisé dans le contexte de l'analyse linguistique ou du traitement automatique des langues.

#### Feuille de route:

- Etat de l'art rapide sur le web
  - Nooj
  - HuggingFace
- Choix d'une base de données gratuite open source
  - Dictionnaire de l’Académie française de 1932-35 (8e édition) > Non adapté (J'enrage!) ❌
  - Lexique Le-Dm > ✔️
  - Morphalou > Pour une utilisation plus riche 💡
- Créer une base de données de noms communs étiquetés par genre
- Faire une analyse des données 🔬
- Créer un modèle de classification de genre avec Pytorch
- Entrainer le modèle et l'optimiser, puis tester le modèle
- créer un modèle de génération de pseudo-mots, puis tester le modèle
- Créer un appli Streamlit puis la publier 🌐
- Un peu de Web scrapping pour imiter le style des sources
- Enrichir avec une analyse de l'usage du genre du mot covid 😷
- Enrichir avec une liste de mots générés selon plusieurs critères en entrée :construction:
- Approche cartographique :construction:
"""

st.markdown(md)
st.sidebar.markdown("# Méthodologie :toolbox:")