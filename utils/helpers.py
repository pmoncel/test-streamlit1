import polars as pl
from data.loader import load_conseillers_municipaux

#dans l'interface on peut le libellé du département ou la fonction
#on veut retourner la liste des conseillers municipaux de ce département ou de cette fonction
def get_conseillers_municipaux(departement, fonction):
    df = load_conseillers_municipaux()
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