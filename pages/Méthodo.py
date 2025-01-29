import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )


md= """
### Genrage

Classificateur de genre : Utilisé dans le contexte de l'analyse linguistique ou du traitement automatique des langues.
Utiliser Pytorch

Feuille de route:

- faire un état de l'art rapide sur le web
  - Nooj
  - HuggingFace
- choisir une base de données gratuite open source
  - Dictionnaire de l’Académie française de 1932-35 (8e édition) > Non adapté
  - lexique Le-Dm > Ok
  - Morphalou > Pour une utilisation plus riche
- créer une base de données de noms communs étiquetés par genre
- faire une analyse des données
"""

st.markdown(md)
st.sidebar.markdown("# Méthodologie :toolbox:")