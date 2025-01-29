import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )

md = """
## Genrage

#### Classificateur de genre : Utilisé dans le contexte de l'analyse linguistique ou du traitement automatique des langues.

#### Predit si un nom français donné est typiquement masculin ou féminin

---

### Sources

---

* LE DM, A FRENCH DICTIONARY FOR NOOJ - FRANÇOIS Trouilleux [https://www.ortolang.fr/market/lexicons/le-dm](https://www.ortolang.fr/market/lexicons/le-dm)
* Tutoriels Pytorch [pytorch.org](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial)
* Dépot NLP-Genrage sur mon github https://github.com/Fran-6/NLP_Genrage

"""

st.markdown(md)
st.sidebar.markdown("# Sources :books:")