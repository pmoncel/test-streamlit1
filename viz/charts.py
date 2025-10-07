#Bibliothèque de haut niveau construite au-dessus de Plotly.
#simple et concise
import plotly.express as px
import polars as pl

def repartition_par_sexe(df):
    # Crée un graphique en camembert de la répartition par sexe
    if df is None or df.is_empty():
        return None
    
    # Compter les occurrences par sexe
    df_count = (df
                .group_by("Code sexe")
                .agg(pl.count().alias("Nombre"))
                .sort("Code sexe"))
    
    # Convertir en pandas pour Plotly
    df_pandas = df_count.to_pandas()
    
    return px.pie(
        df_pandas, 
        values='Nombre',
        names='Code sexe',
        title="Répartition par sexe",
        color_discrete_sequence=['#4169E1', '#FF69B4']
    )


def repartition_par_csp(df, top_n=50):
    # Crée un graphique en barres de la répartition par CSP
    if df is None or df.is_empty():
        return None
    
    # Compter les occurrences par CSP
    df_count = (df
                .filter(pl.col("Libellé de la catégorie socio-professionnelle").is_not_null())
                .group_by("Libellé de la catégorie socio-professionnelle")
                .agg(pl.count().alias("Nombre"))
                .sort("Nombre", descending=True)
                .head(top_n))
    
    # Convertir en pandas pour Plotly
    df_pandas = df_count.to_pandas()
    
    fig = px.bar(
        df_pandas,
        x='Nombre',
        y='Libellé de la catégorie socio-professionnelle',
        title=f"Top {top_n} catégories socio-professionnelles",
        orientation='h',
        color='Nombre',
        color_continuous_scale='Blues',
        height=600
    )
    
    # Personnaliser l'affichage des libellés
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},  # Trier par ordre croissant
        margin={'l': 200}  # Marge gauche pour les libellés longs
    )
    
    return fig