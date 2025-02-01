import streamlit as st
from utils.classifier import set_classifier, evaluation, check_input_text, allowed_characters

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
    else:
        for lex in lexemes:
            idx, pourcentage = evaluation(lex, rnn)
            genre = genres[idx]
            sortie = "Le lexème '{}' est prédit comme {} à {:.1%}".format(lex, genre, pourcentage)
            st.markdown(sortie)


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
        # st.write("Entrez un nom à classer\n\n")
        lexeme = st.text_input(
            "Entrez un nom à classifier et cliquez sur le bouton",
            "covid ; anagramme ; ure ; Ket-Bra; quelqu'un ; noeud",
            help="mots séparés par ';' en caractères alphabétiques + accents, tiret, espace et apostrophe")

    with col2:
        # st.markdown("###### Puis cliquez sur le bouton")
        st.markdown('<p style="font-size: 7px;"> -</p>', unsafe_allow_html=True)

        if st.button("genderize") or EXEC:
            stream_data()

        EXEC = False        
st.markdown("---")



st.sidebar.markdown("# Accueil :house:")
# st.sidebar.markdown("# sources :eyes:")