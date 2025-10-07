import streamlit as st
from data.loader import list_departements, list_fonctions
from utils.helpers import get_conseillers_municipaux
from viz.charts import repartition_par_sexe, repartition_par_csp, distribution_par_age

st.title("Analyse des données des Conseillers Municipaux (12 juin 2025)")
st.set_page_config("Analyse des Conseillers Municipaux", layout="wide") #title and layout

departement = st.sidebar.selectbox("Département", list_departements())
fonction = st.sidebar.selectbox("Fonction", list_fonctions())

df = get_conseillers_municipaux(departement, fonction)


st.markdown(
    """ 
    *Analyse des données des Conseillers Municipaux d'après fichier csv sur https://www.data.gouv.fr/*

    App dans le cadre de la formation Dev IA d'Ecole Alyra Octobre 2025. 
    """
)


titre_departement = 'Tous les départements'
titre_fonction = ' et pour toutes les fonctions'
if departement != '--Tous--':
    titre_departement = f'Département : {departement}'
if fonction != '--Tous--':
    titre_fonction = f' et Fonction : {fonction}'

st.markdown(f"<h2 style='font-weight: bold; color: #1f77b4;'>{titre_departement} {titre_fonction}</h2>", unsafe_allow_html=True)

nombre_elus = df.shape[0]
st.markdown(f"<h3 style='font-weight: bold; color: #1f77b4;'>Nombre d'élus : {nombre_elus}</h3>", unsafe_allow_html=True)

# Répartir les graphiques sur 2 colonnes avec une marge
col1, col_margin, col2 = st.columns([2, 0.1, 2])

with col1:
    with st.container(border=True):
        st.plotly_chart(repartition_par_sexe(df), use_container_width=True)

with col_margin:
    # Colonne vide pour créer une marge
    st.write("")
with col2:
    with st.container(border=True):
        st.plotly_chart(repartition_par_csp(df), use_container_width=True)

with col1:
    with st.container(border=True):
        st.plotly_chart(distribution_par_age(df), use_container_width=True)
with col_margin:
    # Colonne vide pour créer une marge
    st.write("")
#On lancera par streamlit run app.py

