import polars as pl
from data.loader import load_conseillers_municipaux
from datetime import datetime

#dans l'interface on peut le libellé du département ou la fonction
#on veut retourner la liste des conseillers municipaux de ce département ou de cette fonction
def get_conseillers_municipaux(departement, fonction):
    df = load_conseillers_municipaux()

    # Calculer l'âge à partir de la date de naissance
    if "Date de naissance" in df.columns:
        # Convertir la colonne date de naissance en format date
        df = df.with_columns([
            pl.col("Date de naissance").str.to_date("%d/%m/%Y").alias("Date_naissance")
        ])
        
        # Calculer l'âge en années
        current_date = datetime.now()
        df = df.with_columns([
            ((current_date - pl.col("Date_naissance")).dt.total_days() / 365.25).round(0).cast(pl.Int32).alias("Âge")
        ])
    
    if departement != '--Tous--':
        df = df.filter(pl.col("Libellé du département") == departement)
    if fonction != '--Tous--':
        # dans le fichier csv, la fonction est dans la colonne "Libellé de la fonction"
        # pour Maire, on doit filtrer sur "Maire"
        # pour Adjoint au maire, on doit filtrer sur LIKE "adjoint au maire"
        # pour Conseiller municipal, on doit filtrer sur vide
        if fonction == 'Maire':
            df = df.filter(pl.col("Libellé de la fonction") == 'Maire')
        elif fonction == 'Adjoint au maire':
            df = df.filter(pl.col("Libellé de la fonction").str.contains("adjoint au Maire"))
        elif fonction == 'Conseiller municipal':
            df = df.filter(pl.col("Libellé de la fonction").is_null())
    return df