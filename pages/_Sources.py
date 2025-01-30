import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )

md = """
### Sources

---

* LE DM, A FRENCH DICTIONARY FOR NOOJ - FRANÇOIS Trouilleux [https://www.ortolang.fr/market/lexicons/le-dm](https://www.ortolang.fr/market/lexicons/le-dm)
* Tutoriels Pytorch [pytorch.org](https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial)
* Dépot NLP-Genrage sur mon github https://github.com/Fran-6/NLP_Genrage
* D'après Google Trends https://trends.google.fr/trends/explore?date=today%205-y&geo=FR&q=le%20covid,la%20covid,un%20covid,une%20covid&hl=fr%2F 
* Académie Française 🕸️ https://www.dictionnaire-academie.fr/ 
"""

st.markdown(md)
st.sidebar.markdown("# Sources :books:")