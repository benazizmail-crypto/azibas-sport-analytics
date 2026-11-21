REQUIRED_COLUMNS=["sport","event","home_rate","away_rate"]

def validate_event_frame(df):
    missing=[c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing: return ["Colonnes obligatoires absentes : "+", ".join(missing)]
    if df.empty: return ["Le fichier ne contient aucune ligne."]
    if df["event"].isna().any(): return ["Chaque ligne doit avoir un nom de rencontre."]
    return []
