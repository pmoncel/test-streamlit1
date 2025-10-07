import requests
from io import BytesIO
import polars as pl
import streamlit as st
from constant.config import DATASET_URL

@st.cache_data
def load_conseillers_municipaux():
    # Charge les données des conseillers municipaux
    response = requests.get(DATASET_URL)
    response.raise_for_status()
    df = pl.read_csv(
        BytesIO(response.content),
        truncate_ragged_lines=True,  # ← Ajoutez cette option
        ignore_errors=True,           # Ignore les erreurs de parsing
        separator=";",
        has_header= True
    )
    return df


@st.cache_data
def list_departements():
    """
    Charge les données et retourne une liste triée des départements
    """
    df = load_conseillers_municipaux()
    
    # Extraire les départements uniques de la colonne 'Libellé du département'
    departements = (df
                    .filter(pl.col("Libellé du département").is_not_null())
                    .select("Libellé du département")
                    .unique()
                    .sort("Libellé du département"))
    
    # Convertir en liste Python
    list_departements = departements.to_series().to_list()
    
    # Ajouter '--Tous--' au début de la liste
    list_departements = ['--Tous--'] + list_departements

    return list_departements


@st.cache_data
def list_fonctions():
    list_fonctions = ['--Tous--', 'Maire', 'Adjoint au maire', 'Conseiller municipal']
    return list_fonctions