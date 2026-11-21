# AZIBAS SPORT ANALYTICS PRO — v2.1

## Ce que contient ce dépôt
- Interface web Streamlit.
- API FastAPI (`/health`, `/analyze`).
- Modèle football Poisson indépendant pour 1X2, buts et BTTS.
- Modèle de comptage Poisson simplifié pour corners/cartons, sous réserve de moyennes d'entrée.
- Calcul de cote juste, value et espérance par unité.
- Import CSV, export des résultats, tests automatisés et Docker.
- Interfaces abstraites pour connecter plus tard des fournisseurs de calendriers, statistiques et cotes.

## Démarrage local
```bash
python -m venv .venv
# Windows : .venv\Scripts\activate
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

API :
```bash
uvicorn api:app --reload
```
Documentation API : http://127.0.0.1:8000/docs

Tests :
```bash
pytest -q
```

Docker :
```bash
docker compose up --build
```

## Déploiement web
Le projet est prêt à être poussé dans un dépôt GitHub puis publié avec Streamlit Community Cloud (fichier principal `app.py`). Une autre option consiste à déployer le conteneur Docker sur un hébergeur cloud. Le déploiement effectif nécessite un compte hébergeur et une autorisation d'accès ; aucun compte n'est créé ou modifié par ce programme.

## Données et limites
- Les exemples visibles dans l'interface sont explicitement fictifs.
- Aucun flux live n'est connecté dans cette version.
- Aucune clé API n'est fournie. Ne jamais mettre les secrets dans le code ou le navigateur.
- Le moteur ne génère des marchés que pour le football, car aucun modèle validé pour les autres sports n'est livré ici. Les interfaces sont prévues pour ajouter les autres disciplines sans inventer de prédictions.
- Le modèle Poisson indépendant est une baseline, pas une prévision garantie. Il doit être calibré et testé sur des historiques réels avant usage décisionnel.
- Les marchés corners/cartons sont des distributions de comptage simplifiées, dépendantes de moyennes fiables.
- La value calculée est théorique, avant limites de mise, commissions, erreurs de cote, marge bookmaker et corrélation.
- Les combinés ne doivent pas être évalués par simple multiplication si les sélections sont dépendantes.
- Le projet ne place aucun pari automatiquement.

## Prochaine étape de production
Configurer les fournisseurs sous licence, ajouter des adaptateurs authentifiés, stocker les données horodatées dans PostgreSQL, entraîner/calibrer les modèles sport/marché, effectuer des backtests temporels et surveiller la qualité des flux.
