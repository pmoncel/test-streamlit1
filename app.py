import streamlit as st
from data.loader import load_conseillers_municipaux, list_departements, list_fonctions
from utils.helpers import get_conseillers_municipaux
from viz.charts import repartition_par_sexe, repartition_par_csp

st.title("Analyse des données des Conseillers Municipaux")
st.set_page_config("Analyse des Conseillers Municipaux", layout="wide") #title and layout

departement = st.sidebar.selectbox("Département", list_departements())
fonction = st.sidebar.selectbox("Fonction", list_fonctions())

df = get_conseillers_municipaux(departement, fonction)

# Répartir les graphiques sur 2 colonnes avec une marge
col1, col_margin, col2 = st.columns([2, 0.5, 2])

with col1:
    st.plotly_chart(repartition_par_sexe(df), use_container_width=True)
with col_margin:
    # Colonne vide pour créer une marge
    st.write("")
with col2:
    st.plotly_chart(repartition_par_csp(df), use_container_width=True)


#On lancera par streamlit run app.py