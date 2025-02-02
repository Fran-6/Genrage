import streamlit as st
from streamlit_theme import st_theme
from utils.classifier import set_classifier, evaluation, check_input_text, allowed_characters
from utils.autres import get_mots
import pandas as pd
import numpy as np

# Initialisations de paramètres
EXEC = True
# device = set_cuda()
genres = ["féminin", "masculin"]
rnn = set_classifier()
mots_f, mots_m, mots_fm = get_mots()
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
        col_f = []
        col_m = []
        col_faux = []
        col_miss = []
        for lex in lexemes:
            col_f.append(lex in mots_f)
            col_m.append(lex in mots_m)
            col_miss.append(lex not in set(mots_fm))
                       
            idx, pourcentage = evaluation(lex, rnn)
            col_genre.append(genres[idx])
            col_pourcent.append(pourcentage*100)
            col_faux.append((idx==0 and (lex not in mots_f)) or (idx==1 and (lex not in mots_m)) and lex in mots_fm)

        
        df = pd.DataFrame(
            {
                "name": lexemes,
                "genre": col_genre,
                "pourcent": col_pourcent,
                "faux": col_faux,
                "col_f": col_f,
                "col_m": col_m,
                "col_miss": col_miss

            }
        )
        # Function to color text based on 'Score'
        def color_text(val):
            color = 'red' if val else 'green'
            return f'color: {color}'

        
        # theme = st_theme()
        # st.write(theme)

        st.dataframe(

            df.style.highlight_between(color= "#fff5f5",left=49, right=60,axis=0,subset=["pourcent"]),

            column_config={
                "name": st.column_config.TextColumn(
                    label="Lexème",

                    width=200,),
                "genre": st.column_config.TextColumn(
                    label="Genre prédit",
                    help="D'après de réseau de neurones récurrent",
                    width=100,),
                "pourcent": st.column_config.NumberColumn(
                    label="  %",
                    help="Confiance du modele",
                    format="%0.1f",
                    width=50,), 
                "faux": st.column_config.CheckboxColumn(
                            "Erreur",
                            help="Prédiction du réseau de neurones récurrent fausse relativement à la base de données Le-DM",
                            ),              
                "col_f": st.column_config.CheckboxColumn(
                            "Fem.",
                            help="nom féminin présent dans la base de données Le-DM",
                            ),
                "col_m": st.column_config.CheckboxColumn(
                            "Masc.",
                            help="nom masculin présent dans la base de données Le-DM",
                            ),
                "col_miss": st.column_config.CheckboxColumn(
                            "Manquant",
                            help="nom présent dans la base de données Le-DM",
                            ),                                                        
                },hide_index=True)


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
            "Entrez les noms à classifier puis cliquez sur le bouton Genrage",
            "covid ; anagramme ; ure ; sot-l'y-laisse ; noeud;a priori;après-midi;stalactite",
            help="mots séparés par ';' en caractères alphabétiques + accent, tiret, n tilde, cédille, tréma, espace et apostrophe",
            max_chars=300,)

        if st.button("Genrage") or EXEC:
            stream_data()

        EXEC = False        

st.sidebar.markdown("# Accueil :house:")
# st.sidebar.markdown("# sources :eyes:")