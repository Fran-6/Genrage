import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )

md = """
### Sources

---

"""


st.markdown(md)

st.link_button(label="Le-DM, A FRENCH DICTIONARY FOR NOOJ - FRANÇOIS Trouilleux",
               url="https://www.ortolang.fr/market/lexicons/le-dm",
                icon="🗂") 


st.link_button(label="Tutoriels Pytorch",
               url="https://pytorch.org/tutorials/intermediate/char_rnn_classification_tutorial",
                icon="🔥") 


st.link_button(label="Dépot NLP-Genrage sur mon github",
               url="https://github.com/Fran-6/NLP_Genrage",
                icon="🛠") 

st.link_button(label="Google Trends",
               url="https://trends.google.fr/trends/explore?date=today%205-y&geo=FR&q=le%20covid,la%20covid,un%20covid,une%20covid&hl=fr%2F",
                icon="📈") 

st.link_button("Académie Française", "https://www.dictionnaire-academie.fr/", icon="🕸️") 

st.sidebar.markdown("# Sources :books:")