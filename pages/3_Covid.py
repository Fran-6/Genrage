import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Genrage",  # Title on the browser tab
    layout="wide",
    page_icon=":fr:"   # Use an emoji or a local image path
    )


md= """
### Dit-on le ou la COVID ?

#### L'usage des internautes d'après Google Trends:
"""
# https://trends.google.fr/trends/explore?date=today%205-y&geo=FR&q=le%20covid,la%20covid&hl=fr/
# Chemin vers le fichier HTML
file_path = './pages/nepasdire.html'

# Ouvrir le fichier en mode lecture
with open(file_path, 'r', encoding='utf-8') as file:
    # Lire le contenu du fichier
    html_content = file.read()

st.markdown(md)

histo_covid = pd.read_csv('./data/multiTimeline.csv', sep=',', skiprows=2)
histo_covid.columns = ['semaine', 'le', 'la']

histo_covid['le'] = histo_covid['le'].apply(lambda x: '1' if x == '<\xa01' else x)
histo_covid['la'] = histo_covid['la'].apply(lambda x: '1' if x == '<\xa01' else x)

# Convert Column1 to datetime
histo_covid['semaine'] = pd.to_datetime(histo_covid['semaine'])

# Convert Column2 and Column3 to float
histo_covid['le'] = histo_covid['le'].astype(float)
histo_covid['la'] = histo_covid['la'].astype(float)

st.line_chart(histo_covid, x="semaine", y=["le", "la"], color=["#00F","#F00"], x_label="")

st.markdown(
    """<h3>Selon l'académie française</h3><a href="https://www.academie-francaise.fr/search/node/covid/">
    <img src="data:./images/logo.png;base64,{}" width="411">
    </a><p>""".format(
        base64.b64encode(open("./images/logo.png", "rb").read()).decode()
    ),
    unsafe_allow_html=True,
)

st.markdown("---")

st.html(html_content)

css="""
<style>
    [data-testid="stHtml"] {

        padding: 20px;
        border-radius: 20px;
        border: 1px solid #ccc;       
        background: #FCFCEC;
        color: #FFFFFF"


    }
</style>
"""
st.write(css, unsafe_allow_html=True)


st.sidebar.markdown("# Covid 😷")