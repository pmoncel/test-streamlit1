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

# Créer un graphique d'une pyramide d'âges et par sexe
def distribution_par_age(df):
    if df is None or df.is_empty():
        return None
    
# Créer un graphique d'une pyramide d'âges et par sexe
def distribution_par_age(df):
    if df is None or df.is_empty():
        return None
    
    # Filtrer les âges au-delà de 100 ans
    df_filtered = df.filter(pl.col("Âge") <= 100)
    
    # Créer des tranches d'âges de 5 en 5 ans
    df_with_tranches = df_filtered.with_columns([
        (pl.col("Âge") // 5 * 5).alias("Tranche_age_debut"),
        ((pl.col("Âge") // 5 * 5) + 4).alias("Tranche_age_fin")
    ]).with_columns([
        (pl.col("Tranche_age_debut").cast(pl.Utf8) + "-" + pl.col("Tranche_age_fin").cast(pl.Utf8)).alias("Tranche_age")
    ])
    
    # Compter les occurrences par tranche d'âge et par sexe
    df_count = (df_with_tranches
                .group_by("Tranche_age", "Tranche_age_debut", "Code sexe")
                .agg(pl.count().alias("Nombre"))
                .filter(pl.col("Nombre") > 0)  # Filtrer les tranches sans valeurs
                .sort("Tranche_age_debut"))
    
    # Créer une vraie pyramide : hommes à gauche (valeurs négatives), femmes à droite (valeurs positives)
    df_pyramide = df_count.with_columns([
        pl.when(pl.col("Code sexe") == "M")
        .then(-pl.col("Nombre").cast(pl.Int32))  # Convertir en Int32 avant la négation
        .otherwise(pl.col("Nombre").cast(pl.Int32))  # Convertir en Int32 pour cohérence
        .alias("Nombre_pyramide")
    ])
    
    # Convertir en pandas pour Plotly
    df_pandas = df_pyramide.to_pandas()
    
    fig = px.bar(
        df_pandas,
        x='Nombre_pyramide',
        y='Tranche_age',
        color='Code sexe',
        title="Pyramide par âges et sexe par tranches de 5 ans",
        orientation='h',
        color_discrete_sequence=['#4169E1', '#FF69B4']
    )

    # Personnalisation pour une vraie pyramide
    fig.update_layout(
        xaxis_title="Population (Hommes ← | Femmes →)",
        yaxis_title="Tranches d'âges",
        yaxis=dict(categoryorder="array", categoryarray=sorted(df_pandas['Tranche_age'].unique(), key=lambda x: int(x.split('-')[0]))),
        xaxis=dict(
            tickformat=",d",
            zeroline=True,
            zerolinecolor='black',
            zerolinewidth=2
        ),
        hovermode="y",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Ajouter une ligne verticale au centre
    fig.add_vline(x=0, line_dash="solid", line_color="black", line_width=2)
    
    return fig

    
    # Personnaliser l'affichage des libellés