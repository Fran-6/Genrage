import streamlit as st

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )


md= """
### Apprentissages et perspectives

##### Mise en pratique des réseaux de neurones

#### Points clé:

- Linguistique
  - Nooj
  - HuggingFace
  
\
&nbsp;
  
- data science
  - préparation des données, SQL
  - pytorch
  
\
&nbsp;
  
- deep learning
  - RNN
  
\
&nbsp;
  
- code
  - Streamlit API
  - Python:
      - Pandas
      - numpy
  - HTML, CSS, webscrapping

"""

st.markdown(md)
st.sidebar.markdown("""# Retour d'expérience 📝""")