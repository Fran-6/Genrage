import streamlit as st
from utils.classifier import set_classifier, evaluation, check_input_text, allowed_characters
import pandas as pd

# Initialisations de paramètres
EXEC = True
# device = set_cuda()
genres = ["féminin", "masculin"]
rnn = set_classifier()
# Initialisation des fonctions
def stream_data():
    answer, lexemes = check_input_text(lexeme)
    if answer is not None:
        st.markdown(answer)
        return answer
    elif len(lexemes) == 1:
        idx, pourcentage = evaluation(lexemes[0], rnn)
        genre = genres[idx]
        sortie = "Le lexème '{}' est prédit comme {} à {:.1%}".format(lexemes[0], genre, pourcentage)
        st.markdown(sortie)
    elif lexemes[0] == "old":
        for lex in lexemes:
            idx, pourcentage = evaluation(lex, rnn)
            genre = genres[idx]
            sortie = 'Le lexème "{}" est prédit comme {} à {:.1%}'.format(lex, genre, pourcentage)
            st.markdown(sortie)

    else:
        col_genre = []
        col_pourcent = []
        for lex in lexemes:
            idx, pourcentage = evaluation(lex, rnn)
            col_genre.append(genres[idx])
            col_pourcent.append(pourcentage*100)
        
        df = pd.DataFrame(
            {
                "name": lexemes,
                "genre": col_genre,
                "pourcent": col_pourcent
            }
        )
        st.dataframe(
            df,
            column_config={
                "name": "Lexème",
                "genre": "Genre prédit",
                "pourcent": st.column_config.NumberColumn(
                    label="%",
                    help="Fiabilite selon le modele",
                    format="%.1f",
                    width=50,
                    
                ),

            },hide_index=True,)




# Configuration initiale
# st.set_page_config(page_title="Genrage", layout="wide")
# Set the page configuration
st.set_page_config(
    page_title="Genrage Streamlit",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:",   # Use an emoji or a local image path
)
st.markdown("""# Le genre des mots selon leur morphologie""")

with st.container():
    # Créer des colonnes à l'intérieur du conteneur
    col1, col2 = st.columns([1, 3])
    
    with col1:
        pass

    with col2:
        # st.write("Entrez un nom à classer\n\n")
        lexeme = st.text_area(
            "Entrez les noms à classifier puis cliquez sur le bouton Genderize",
            "covid ; anagramme ; ure ; Ket-Bra; quelqu'un ; noeud;a priori;guet-apens;curriculum vitae",
            help="mots séparés par ';' en caractères alphabétiques + accents, tiret, cédille, espace et apostrophe",
            max_chars=300)

        if st.button("Genderize") or EXEC:
            stream_data()

        EXEC = False        

st.sidebar.markdown("# Accueil :house:")
# st.sidebar.markdown("# sources :eyes:")