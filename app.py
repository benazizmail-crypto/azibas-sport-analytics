import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from azibas.engine import analyze_event
from azibas.schemas import validate_event_frame

st.set_page_config(page_title="AZIBAS SPORT ANALYTICS", page_icon="📊", layout="wide")
st.title("📊 AZIBAS SPORT ANALYTICS")
st.caption("PRO · Multi-sports intelligence · Analyse, simulation et suivi des modèles")
st.warning("Les pronostics réels exigent des données fiables et des cotes actuelles. Sans fournisseur connecté, l'application fonctionne en mode import/démonstration et n'invente pas de rencontres.")

with st.sidebar:
    st.header("Paramètres")
    profile = st.selectbox("Profil d'analyse", ["Balanced", "Safe", "Value"])
    simulations = st.select_slider("Simulations Monte-Carlo", options=[5000, 10000, 25000, 50000, 100000], value=25000)
    min_value = st.slider("Value minimale (%)", 0, 30, 5) / 100
    min_odds = st.number_input("Cote minimale", min_value=1.01, value=1.80, step=.05)
    max_odds = st.number_input("Cote maximale", min_value=1.01, value=10.0, step=.10)
    st.divider()
    uploaded = st.file_uploader("Importer les événements (CSV)", type=["csv"])
    demo = st.checkbox("Charger les exemples fictifs", value=True)

st.subheader("Centre de contrôle")
m1,m2,m3,m4=st.columns(4)
m1.metric("Sports supportés par architecture", "10")
m2.metric("Simulations / marché", f"{simulations:,}".replace(",", " "))
m3.metric("Mode données", "Import + démo")
m4.metric("Heure UTC", datetime.now(timezone.utc).strftime("%H:%M"))

frames=[]
if uploaded:
    try:
        user_df=pd.read_csv(uploaded)
        errs=validate_event_frame(user_df)
        if errs: st.error("CSV invalide : "+" | ".join(errs))
        else: frames.append(user_df.assign(data_status="Import utilisateur"))
    except Exception as e:
        st.error(f"Lecture impossible : {e}")

if demo:
    frames.append(pd.DataFrame([
      {"sport":"Football","event":"Équipe exemple A – Équipe exemple B","home_rate":1.55,"away_rate":1.05,"corners_mean":9.8,"cards_mean":4.1,"odds_home":1.95,"odds_draw":3.4,"odds_away":4.0,"odds_over25":1.9,"odds_under25":1.95,"odds_btts":1.85,"odds_over95_corners":1.9,"odds_over35_cards":1.9,"data_status":"DÉMO FICTIVE"},
      {"sport":"Football","event":"Équipe exemple C – Équipe exemple D","home_rate":1.15,"away_rate":1.35,"corners_mean":10.1,"cards_mean":3.5,"odds_home":2.8,"odds_draw":3.1,"odds_away":2.5,"odds_over25":1.95,"odds_under25":1.9,"odds_btts":1.8,"odds_over95_corners":1.88,"odds_over35_cards":2.0,"data_status":"DÉMO FICTIVE"}
    ]))
if not frames:
    st.info("Ajoute un CSV ou active les exemples fictifs pour tester le moteur.")
    st.stop()

events=pd.concat(frames,ignore_index=True)
out=[]
for _,event in events.iterrows():
    out.extend(analyze_event(event.to_dict(), simulations))
df=pd.DataFrame(out)
if not df.empty:
    df=df[(df.odds>=min_odds)&(df.odds<=max_odds)]
    if profile=="Safe": df=df[df.probability>=.65]
    elif profile=="Value": df=df[df.value>=max(min_value,.10)]
    else: df=df[df.value>=min_value]
    df=df.sort_values(["value","probability"],ascending=False)

a,b,c=st.columns(3)
a.metric("Rencontres fournies",events.event.nunique())
b.metric("Marchés réellement modélisés",len(out))
c.metric("Sélections dépassant le seuil",len(df))
st.subheader("Résultats du scanner")
if df.empty:
    st.info("Aucun marché ne satisfait les critères ou aucun modèle n'est disponible pour les données fournies.")
else:
    view=df.copy()
    view["probability"]=view.probability.map(lambda x:f"{x:.1%}")
    view["fair_odds"]=view.fair_odds.map(lambda x:f"{x:.2f}")
    view["value"]=view.value.map(lambda x:f"{x:.1%}")
    view["ev_per_unit"]=view.ev_per_unit.map(lambda x:f"{x:.3f}")
    st.dataframe(view, use_container_width=True, hide_index=True)
    st.download_button("Exporter les résultats CSV",df.to_csv(index=False).encode(), "azibas_scan.csv","text/csv")

st.subheader("Gestion prudente de bankroll")
bank=st.number_input("Bankroll (FCFA)",min_value=0,value=50000,step=5000)
fraction=st.slider("Mise indicative (% bankroll)",0.0,2.0,0.5,0.1)/100
stake=bank*fraction
st.metric("Mise indicative plafonnée",f"{stake:,.0f} FCFA")
st.caption("Ce montant est une limite de gestion indicative, pas une recommandation de pari. Les modèles ne garantissent aucun résultat.")

with st.expander("CSV — format attendu"):
    st.code("sport,event,home_rate,away_rate,corners_mean,cards_mean,odds_home,odds_draw,odds_away,odds_over25,odds_under25,odds_btts,odds_over95_corners,odds_over35_cards\\nFootball,Club A - Club B,1.5,1.1,9.6,4.0,2.0,3.2,3.8,1.9,1.9,1.8,1.9,1.9",language="csv")
    st.write("Les colonnes de cote sont facultatives. Sans cote fournie, le marché n'est pas évalué.")
st.caption("AZIBAS PRO · Aucun fournisseur de données live n'est connecté dans ce pack.")
