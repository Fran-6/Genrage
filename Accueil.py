import streamlit as st
# from streamlit_theme import st_theme
from utils.classifier import set_classifier, evaluation, check_input_text, allowed_characters
from utils.generator import set_generator, generate
from utils.generator import all_letters
from utils.autres import get_mots
import pandas as pd
import numpy as np
import random


from streamlit import session_state as ss

# Set the page configuration
st.set_page_config(
    page_title="Genrage Streamlit",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:",   # Use an emoji or a local image path
)

# Initialisations de paramètres
EXEC = True


genres = ["féminin", "masculin"]
mots_f, mots_m, mots_epi, mots_fx, mots_mx, mots_fm = get_mots()

set_f, set_m, set_fm = set(mots_f), set(mots_m), set(mots_fm)

liste_de_mots = ["covid","anagramme","ure","sot-l'y-laisse", "noeud",
                "a priori", "après-midi", "stalactite", "xylite",
                "adénofibromerien", "imprévisibilitière", "télé-détectioneuse", "caille-laiton",
                "xateure-teuterre", "descendancerie", "coupé-colléonore", "herophyme","zoriche"]
if "input_txt" not in ss: ss.input_txt = "covid ; anagramme ; ure ; sot-l'y-laisse ; noeud ; a priori ; après-midi ; stalagtite"
if "col_genres_rnn" not in ss: ss.col_genres_rnn = ["-"]*len(ss.input_txt.split(";")) 
if "rnn_txt" not in ss: ss.rnn_txt = ""
listes_dict = {
    # fx, epi, mx
    (True, True, True): mots_fm,
    (True, True, False): mots_f,
    (True, False, True): mots_fx + mots_mx,
    (True, False, False): mots_fx,
    (False, True, True): mots_m,
    (False, True, False): mots_epi,
    (False, False, True): mots_mx,
    (False, False, False): [],
}
liste_genres_dict = {
    # fx, epi, mx
    (True, True, True): ['fs', 'ms'],
    (True, True, False): ['fs', 'ms'],
    (True, False, True): ['fs', 'ms'],
    (True, False, False): ['fs'],
    (False, True, True): ['fs', 'ms'],
    (False, True, False): ['fs', 'ms'],
    (False, False, True): ['ms'],
    (False, False, False): ['fs', 'ms'],  
}

rnn = set_classifier()
gen_rnn = set_generator()

# Initialisation des fonctions

def stream_data():
    lexeme = ss.lexeme
    answer, lexemes =  check_input_text(lexeme) # ss.id_txt # lexeme 
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
        col_rnn = []
        for lex in lexemes:
            col_f.append(lex in set_f)
            col_m.append(lex in set_m)
            col_miss.append(lex not in set_fm)
                       
            idx, pourcentage = evaluation(lex, rnn)
            col_genre.append(genres[idx])
            col_pourcent.append(pourcentage*100)
            col_faux.append(((idx==0 and (lex not in set_f)) or (idx==1 and (lex not in set_m))) and lex in set_fm)

        if ss.lexeme == ss.rnn_txt:
            col_rnn = ss.col_genres_rnn
            col_faux = [ r!=g for r, g in zip(col_rnn, col_genre)]
        else:
            col_rnn = ["-"]*len(lexemes)
            

        df = pd.DataFrame(
            {
                "name": lexemes,
                "genre": col_genre,
                "pourcent": col_pourcent,
                "faux": col_faux,
                "col_f": col_f,
                "col_m": col_m,
                "col_miss": col_miss,
                "col_rnn": col_rnn,

            }
        )

        st.dataframe(

            df,
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
                            help="Prédiction du réseau de neurones récurrent fausse",
                            ),              
                "col_f": st.column_config.CheckboxColumn(
                            "Fem.",
                            help="Nom féminin présent dans la base de données Le-DM",
                            ),
                "col_m": st.column_config.CheckboxColumn(
                            "Masc.",
                            help="Nom masculin présent dans la base de données Le-DM",
                            ),
                "col_miss": st.column_config.CheckboxColumn(
                            "Manquant",
                            help="Nom absent de la base de données Le-DM",
                            ),
                "col_rnn": st.column_config.TextColumn(
                    label="RNN",
                    help="Genre théorique des pseudo-mots créés par le réseau de neurones récurrent",
                    width=100),
                },hide_index=True, key="id_df")

def stream_gen():
    #
    n = 0 # d
    # choix ":rainbow[pseudo-mots]", "Liste prédéfinie", "Noms communs"
    # fx ,epi, mx de checkbox
    mots = []
    genres_rnn = []
    limit = 0
    if choix == ":rainbow[pseudo-mots]":
        
        while n < number and limit < 100:

            debut = str(random.sample(mots_fm,1)[0]) if txt == "" else txt

            g = random.sample(liste_genres_dict[(fx, epi, mx)], 1)
            g = "".join(g)
    
            mot = generate(gen_rnn, g ,start_letter= debut if debut else "a")
            if mot not in mots:
                mots.append(mot)
                inputs = " ; ".join(mots)
                genres_rnn.append("féminin" if g=="fs" else "masculin" if g=="ms" else "?")
                n += 1
            limit += 1
        print(f"Le générateur à fait {limit} essais pour créer {n} mots différents")
        ss.rnn_txt = inputs

    elif choix == "Liste prédéfinie":
        inputs = random.sample(liste_de_mots, min(len(liste_de_mots), number))
        inputs = " ; ".join(inputs)
        genres_rnn = ["-"]*len(inputs.split(";"))

    elif choix == "Noms communs":
        liste_choisie = listes_dict[(fx, epi, mx)]
        
        if txt != "":
            prefix = txt
            # Filtrer les mots dont les deux premiers caractères sont le préfixe donné
            liste_choisie = [m for m in liste_choisie if m.startswith(prefix)]

        if liste_choisie == []:
            inputs = ""
        else:
            inputs = random.sample(liste_choisie, min(len(liste_choisie), number),)
            inputs = " ; ".join(inputs)
        
    
    ss.col_genres_rnn = genres_rnn
    ss.input_txt = inputs
   
def reset_input():
    ss.input_txt = ""
    
st.markdown("""## Le genre des mots selon leur morphologie""")

with st.container(height=None):
    # Créer des colonnes à l'intérieur du conteneur
    col2, col1 = st.columns([3, 1], border=True)

    with col1:

        txt = st.text_input("Mots commençant par:", "", max_chars=3)
        st.write("The current movie title is", txt)

        choix = st.radio(
            "Générateur de mots",
            [":rainbow[pseudo-mots]", "Liste prédéfinie", "Noms communs"],
            captions=["générés par RNN","","Issus du dictionaire Le-Dm",],)

        with st.container(border=True):
            left, middle, right = st.columns(3)
            fx = left.checkbox("♀️", value=True, disabled=False, key="id_fx",help="Mots féminins") #, help="féminins exclusifs")
            epi = middle.checkbox("🔗", value=True, disabled=False, key="id_epi", help="Mots des deux genres") #, help="mots des 2 genres")
            mx = right.checkbox("♂️", value=True, disabled=False, key="id_mx", help="Mots masculins") #, help="masculins exclusifs")


        number = st.number_input("Nombre de mots à générer", value=10, min_value=1, max_value=20, step=1)

    with col2:
        # st.write("Entrez un nom à classer")
        ss.lexeme = st.text_area(
            label="Entrez les mots puis cliquez sur le bouton Genrage ou 'CTRL+Entrée'",
            value=ss.input_txt,
            help="mots séparés par ';' en caractères alphabétiques + accent, tiret, n tilde, cédille, tréma, espace et apostrophe)",
            max_chars=300, key="id_txt",
            placeholder="Entrez un mot ou des mots à classifier séparés par des ';' (caractères autorisés: alphabétiques + accent, tiret, n tilde, cédille, tréma, espace et apostrophe"            )

        sc1, sc2, sc3 = st.columns((2,1,5))

        sc1.button("Liste de mots aléatoires", on_click=stream_gen) 
        # if sc3.button("Reset"):
        #     reset_input()
        if sc2.button("Genrage") or EXEC:
            EXEC = False
            stream_data()      
            
        sc3.button("Reset", on_click=reset_input)


st.sidebar.markdown("# Accueil :house:")
# st.sidebar.markdown("# sources :eyes:")
