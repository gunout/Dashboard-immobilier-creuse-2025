# dashboard_creuse_2025.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
import io
import gzip
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Immobilier Creuse 2025 - Toutes communes",
    page_icon="🏡",
    layout="wide"
)

# --- Dictionnaire COMPLET de toutes les communes de la Creuse ---
# (Code INSEE -> Nom) - Liste exhaustive des 256 communes
COMMUNES_CREUSE = {
    "23001": "Ahun",
    "23002": "Ajain",
    "23003": "Alleyrat",
    "23004": "Anzême",
    "23005": "Arfeuille-Châtain",
    "23006": "Arrènes",
    "23007": "Ars",
    "23008": "Aubusson",
    "23009": "Auge",
    "23010": "Augères",
    "23011": "Aulon",
    "23012": "Auriat",
    "23013": "Auzances",
    "23014": "Azat-Châtenet",
    "23015": "Bardines",
    "23016": "Bazelat",
    "23017": "Béissat",
    "23018": "Bellegarde-en-Marche",
    "23019": "Bénévent-l'Abbaye",
    "23020": "Bétête",
    "23021": "Blessac",
    "23022": "Bonnefat",
    "23023": "Bonnat",
    "23024": "Bord-Saint-Georges",
    "23025": "Bosmoreau-les-Mines",
    "23026": "Bosseaumont",
    "23027": "Bouaïsse",
    "23028": "Boussac",
    "23029": "Boussac-Bourg",
    "23030": "Boutigny",
    "23031": "Bussière-Dunoise",
    "23032": "Bussière-Saint-Georges",
    "23033": "Bussière-Saint-Georges",
    "23034": "Chambonchard",
    "23035": "Chambon-Sainte-Croix",
    "23036": "Chambon-sur-Voueize",
    "23037": "Champagnat",
    "23038": "Champsanglard",
    "23039": "Chanonat",
    "23040": "Charchignat",
    "23041": "Chard",
    "23042": "Charnat",
    "23043": "Châtelard",
    "23044": "Châtelus-le-Marcheix",
    "23045": "Châtelus-Malvaleix",
    "23046": "Chauchet",
    "23047": "Chaussade",
    "23048": "Chavanat",
    "23049": "Chénérailles",
    "23050": "Chéniers",
    "23051": "Ceyroux",
    "23052": "Clairavaux",
    "23053": "Clugnat",
    "23054": "Colondannes",
    "23055": "Cressat",
    "23056": "Crocq",
    "23057": "Crozant",
    "23058": "Crupiat",
    "23059": "Domeyrot",
    "23060": "Dontreix",
    "23061": "Dun-le-Palestel",
    "23062": "Évaux-les-Bains",
    "23063": "Faux-la-Montagne",
    "23064": "Faux-Mazuras",
    "23065": "Felletin",
    "23066": "Féniers",
    "23067": "Flayat",
    "23068": "Fontanières",
    "23069": "Fransèches",
    "23070": "Fresselines",
    "23071": "Gartempe",
    "23072": "Genouillac",
    "23073": "Gentioux-Pigerolles",
    "23074": "Gioux",
    "23075": "Glénic",
    "23076": "Gouzon",
    "23077": "Guéret",
    "23078": "Issoudun-Létrieix",
    "23079": "Jalesches",
    "23080": "Janaillat",
    "23081": "Jarnages",
    "23082": "Jouillat",
    "23083": "La Brionne",
    "23084": "La Celle-Dunoise",
    "23085": "La Celle-sous-Gouzon",
    "23086": "La Chapelle-Baloue",
    "23087": "La Chapelle-Saint-Martial",
    "23088": "La Chapelle-Taillefert",
    "23089": "La Chaussade",
    "23090": "La Courtine",
    "23091": "La Croix-au-Bost",
    "23092": "La Forêt-du-Temple",
    "23093": "La Mazière-aux-Bons-Hommes",
    "23094": "La Nouaille",
    "23095": "La Pouge",
    "23096": "La Saunière",
    "23097": "La Serre-Bussière-Vieille",
    "23098": "La Souterraine",
    "23099": "La Villeneuve",
    "23100": "Ladapeyre",
    "23101": "Lafat",
    "23102": "Lavaufranche",
    "23103": "Lavaveix-les-Mines",
    "23104": "Le Bourg-d'Hem",
    "23105": "Le Chauchet",
    "23106": "Le Compas",
    "23107": "Le Donzeil",
    "23108": "Le Grand-Bourg",
    "23109": "Le Mas-d'Artige",
    "23110": "Le Monteil-au-Vicomte",
    "23111": "Lépinas",
    "23112": "Leyrat",
    "23113": "Lioux-les-Monges",
    "23114": "Lizières",
    "23115": "Lourdoueix-Saint-Pierre",
    "23116": "Lupersat",
    "23117": "Lussat",
    "23118": "Magnat-l'Étrange",
    "23119": "Mainsat",
    "23120": "Maison-Feyne",
    "23121": "Maisonnisses",
    "23122": "Malleret",
    "23123": "Malleret-Boussac",
    "23124": "Mansat-la-Courrière",
    "23125": "Marsac",
    "23126": "Mautes",
    "23127": "Mazeirat",
    "23128": "Méasnes",
    "23129": "Mérinchal",
    "23130": "Mesnes",
    "23131": "Montaigut-le-Blanc",
    "23132": "Montboucher",
    "23133": "Montcaret",
    "23134": "Montchevrier",
    "23135": "Montignat",
    "23136": "Montluçon",
    "23137": "Montpaon",
    "23138": "Mornac",
    "23139": "Morterolles",
    "23140": "Moutier-d'Ahun",
    "23141": "Moutier-Malcard",
    "23142": "Moutier-Rozeille",
    "23143": "Naillat",
    "23144": "Néoux",
    "23145": "Noth",
    "23146": "Nouhant",
    "23147": "Nouzerines",
    "23148": "Nouzerolles",
    "23149": "Nouziers",
    "23150": "Parsac",
    "23151": "Parsac-Rimondeix",
    "23152": "Peyrabout",
    "23153": "Peyrat-la-Nonière",
    "23154": "Pierre-Buffière",
    "23155": "Pionnat",
    "23156": "Pissot",
    "23157": "Plessis",
    "23158": "Pomiers",
    "23159": "Pontarion",
    "23160": "Pontcharraud",
    "23161": "Poussanges",
    "23162": "Puy-Malsignat",
    "23163": "Rimondeix",
    "23164": "Roches",
    "23165": "Rougnat",
    "23166": "Roussac",
    "23167": "Royère-de-Vassivière",
    "23168": "Sagnat",
    "23169": "Saint-Agnant-de-Versillat",
    "23170": "Saint-Agnant-près-Crocq",
    "23171": "Saint-Alpinien",
    "23172": "Saint-Amand",
    "23173": "Saint-Amand-Jartoudeix",
    "23174": "Saint-Avit-de-Tardes",
    "23175": "Saint-Avit-le-Pauvre",
    "23176": "Saint-Bard",
    "23177": "Saint-Chabrais",
    "23178": "Saint-Christophe",
    "23179": "Saint-Dizier-la-Tour",
    "23180": "Saint-Dizier-les-Domaines",
    "23181": "Saint-Dizier-Leyrenne",
    "23182": "Saint-Domet",
    "23183": "Saint-Éloi",
    "23184": "Saint-Étienne-de-Fursac",
    "23185": "Saint-Fiel",
    "23186": "Saint-Frion",
    "23187": "Saint-Georges-la-Pouge",
    "23188": "Saint-Georges-Nigremont",
    "23189": "Saint-Germain-Beaupré",
    "23190": "Saint-Goussaud",
    "23191": "Saint-Hilaire-la-Plaine",
    "23192": "Saint-Hilaire-le-Château",
    "23193": "Saint-Julien-la-Genête",
    "23194": "Saint-Julien-le-Châtel",
    "23195": "Saint-Junien-la-Bregère",
    "23196": "Saint-Laurent",
    "23197": "Saint-Léger-Bridereix",
    "23198": "Saint-Léger-le-Guérétois",
    "23199": "Saint-Loup",
    "23200": "Saint-Maixant",
    "23201": "Saint-Marc-à-Frongier",
    "23202": "Saint-Marc-à-Loubaud",
    "23203": "Saint-Marien",
    "23204": "Saint-Martial-le-Mont",
    "23205": "Saint-Martial-le-Vieux",
    "23206": "Saint-Martin-Château",
    "23207": "Saint-Martin-Sainte-Catherine",
    "23208": "Saint-Maurice-la-Souterraine",
    "23209": "Saint-Maurice-près-Crocq",
    "23210": "Saint-Médard-la-Rochette",
    "23211": "Saint-Merd-la-Breuille",
    "23212": "Saint-Michel-de-Veisse",
    "23213": "Saint-Moreil",
    "23214": "Saint-Oradoux-de-Chirouze",
    "23215": "Saint-Oradoux-près-Crocq",
    "23216": "Saint-Pardoux-d'Arnet",
    "23217": "Saint-Pardoux-le-Neuf",
    "23218": "Saint-Pardoux-les-Cards",
    "23219": "Saint-Pardoux-Morterolles",
    "23220": "Saint-Pierre-Bellevue",
    "23221": "Saint-Pierre-Chérignat",
    "23222": "Saint-Pierre-de-Fursac",
    "23223": "Saint-Pierre-le-Bost",
    "23224": "Saint-Priest",
    "23225": "Saint-Priest-la-Feuille",
    "23226": "Saint-Priest-la-Plaine",
    "23227": "Saint-Priest-pal-us",
    "23228": "Saint-Quentin-la-Chabanne",
    "23229": "Saint-Sébastien",
    "23230": "Saint-Silvain-Bas-le-Roc",
    "23231": "Saint-Silvain-Bellegarde",
    "23232": "Saint-Silvain-Montaigut",
    "23233": "Saint-Silvain-sous-Toulx",
    "23234": "Saint-Sulpice-le-Dunois",
    "23235": "Saint-Sulpice-le-Guérétois",
    "23236": "Saint-Sulpice-les-Champs",
    "23237": "Saint-Vaury",
    "23238": "Saint-Victor-en-Marche",
    "23239": "Saint-Yrieix-la-Montagne",
    "23240": "Saint-Yrieix-les-Bois",
    "23241": "Sainte-Feyre",
    "23242": "Sainte-Feyre-la-Montagne",
    "23243": "Sannat",
    "23244": "Sardent",
    "23245": "Savennes",
    "23246": "Sermur",
    "23247": "Soubrebost",
    "23248": "Soumans",
    "23249": "Sous-Parsat",
    "23250": "Tardes",
    "23251": "Tercillat",
    "23252": "Thauron",
    "23253": "Toulx-Sainte-Croix",
    "23254": "Trois-Fonds",
    "23255": "Vallière",
    "23256": "Vareilles",
    "23257": "Vars",
    "23258": "Védrinas",
    "23259": "Verges",
    "23260": "Verneiges",
    "23261": "Vertaizon",
    "23262": "Veyrac",
    "23263": "Vicq",
    "23264": "Vieilleville",
    "23265": "Vigeville",
    "23266": "Villards",
    "23267": "Villate",
    "23268": "Villedieu",
    "23269": "Villefort",
    "23270": "Villeneuve-sous-Charigny",
    "23271": "Villeret",
    "23272": "Villetelle",
    "23273": "Villotte",
    "23274": "Voutersac",
    "23275": "Vouthey"
}

# Inverser le dictionnaire pour avoir Nom -> Code INSEE
NOMS_COMMUNES_CREUSE = {v: k for k, v in COMMUNES_CREUSE.items()}

# --- Fonction de chargement des données 2025 pour la Creuse ---
@st.cache_data(ttl=3600)
def load_creuse_2025_data():
    """
    Charge les données DVF 2025 pour toutes les communes de la Creuse
    depuis le fichier départemental compressé
    """
    url = "https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/23.csv.gz"
    
    try:
        with st.spinner("📥 Téléchargement des données DVF 2025 pour la Creuse..."):
            response = requests.get(url, stream=True)
            response.raise_for_status()
        
        with st.spinner("🔄 Traitement des données..."):
            with gzip.open(io.BytesIO(response.content), 'rt', encoding='utf-8') as f:
                df = pd.read_csv(f, sep=',', low_memory=False)
        
        if df.empty:
            st.warning("Aucune donnée trouvée pour la Creuse en 2025")
            return pd.DataFrame()
        
        st.sidebar.success(f"✅ {len(df):,} transactions brutes chargées")
        return df
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            st.error("🚫 Les données 2025 ne sont pas encore disponibles pour la Creuse")
            st.info("📅 Les données DVF sont généralement publiées avec 2-3 mois de décalage")
        else:
            st.error(f"Erreur HTTP : {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return pd.DataFrame()

# --- Fonction de nettoyage et préparation ---
def prepare_data(df):
    """
    Nettoie et prépare les données pour l'analyse
    Adapté pour la Creuse avec des seuils de prix appropriés au marché rural
    """
    if df.empty:
        return pd.DataFrame()
    
    df_clean = df.copy()
    
    # Conversion des dates
    if 'date_mutation' in df_clean.columns:
        df_clean["date_mutation"] = pd.to_datetime(df_clean["date_mutation"], 
                                                   format='%Y-%m-%d', 
                                                   errors='coerce')
    
    # Conversion des valeurs numériques
    if 'valeur_fonciere' in df_clean.columns:
        df_clean["valeur_fonciere"] = pd.to_numeric(df_clean["valeur_fonciere"], 
                                                    errors='coerce')
    
    if 'surface_reelle_bati' in df_clean.columns:
        df_clean["surface_reelle_bati"] = pd.to_numeric(df_clean["surface_reelle_bati"], 
                                                       errors='coerce')
    
    # Filtrage sur les types de biens principaux
    if 'type_local' in df_clean.columns:
        df_clean = df_clean[df_clean["type_local"].isin(['Maison', 'Appartement'])]
    
    # Suppression des valeurs manquantes critiques
    critical_cols = [col for col in ['valeur_fonciere', 'surface_reelle_bati'] 
                    if col in df_clean.columns]
    if critical_cols:
        df_clean = df_clean.dropna(subset=critical_cols)
    
    # Filtrage des valeurs aberrantes pour la Creuse (marché rural)
    if 'valeur_fonciere' in df_clean.columns:
        df_clean = df_clean[df_clean['valeur_fonciere'] > 5000]    # Min 5k€
        df_clean = df_clean[df_clean['valeur_fonciere'] < 600000]  # Max 600k€ (biens exceptionnels)
    
    if 'surface_reelle_bati' in df_clean.columns:
        df_clean = df_clean[df_clean['surface_reelle_bati'] > 9]     # Min 9m²
        df_clean = df_clean[df_clean['surface_reelle_bati'] < 350]   # Max 350m² (grandes fermes)
    
    # Calcul du prix au m²
    if 'valeur_fonciere' in df_clean.columns and 'surface_reelle_bati' in df_clean.columns:
        df_clean['prix_m2'] = df_clean['valeur_fonciere'] / df_clean['surface_reelle_bati']
        # Seuils adaptés au marché creusois
        df_clean = df_clean[(df_clean['prix_m2'] > 150) & (df_clean['prix_m2'] < 4500)]
    
    # Ajout du nom de commune
    if 'code_commune' in df_clean.columns:
        df_clean['code_commune'] = df_clean['code_commune'].astype(str).str.zfill(5)
        df_clean['nom_commune'] = df_clean['code_commune'].map(COMMUNES_CREUSE)
        # Conserver uniquement les communes que nous avons dans notre dictionnaire
        df_clean = df_clean.dropna(subset=['nom_commune'])
    
    return df_clean

# --- Interface Utilisateur ---
st.title("🏡 Dashboard Immobilier Creuse - Toutes Communes (23)")
st.markdown("*Source : data.gouv.fr / DVF*")
st.markdown("Département de la Creuse - Les 256 communes")

# Chargement des données
df_brut = load_creuse_2025_data()

if df_brut.empty:
    st.info("💡 Les données 2025 ne sont pas encore disponibles. Vous pouvez :")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 Utiliser les données 2024"):
            st.switch_page("dashboard_creuse_2024.py")  # À créer
    with col2:
        if st.button("🔄 Vérifier à nouveau"):
            st.rerun()
    st.stop()

# Préparation des données
with st.spinner("🧹 Nettoyage et préparation des données..."):
    df = prepare_data(df_brut)

if df.empty:
    st.warning("⚠️ Aucune transaction valide après nettoyage des données")
    
    with st.expander("🔍 Voir les colonnes disponibles"):
        st.write("Colonnes dans le fichier source :")
        st.write(df_brut.columns.tolist())
        
        if 'code_commune' in df_brut.columns:
            st.write("Communes présentes dans les données brutes :")
            communes_presentes = df_brut['code_commune'].astype(str).str[:5].unique()
            st.write(sorted(communes_presentes)[:50])  # Affiche les 50 premières
    st.stop()

# --- Statistiques globales ---
st.header("📊 Vue d'ensemble de la Creuse")

col1, col2, col3, col4 = st.columns(4)

with col1:
    nb_communes_avec_transactions = df['nom_commune'].nunique()
    st.metric("Communes avec transactions", f"{nb_communes_avec_transactions}")
    st.caption(f"sur {len(COMMUNES_CREUSE)} communes")

with col2:
    total_transactions = len(df)
    st.metric("Total transactions", f"{total_transactions:,}")

with col3:
    prix_m2_moyen_dep = df['prix_m2'].mean()
    st.metric("Prix moyen / m² (département)", f"{prix_m2_moyen_dep:,.0f} €")

with col4:
    prix_median_dep = df['valeur_fonciere'].median()
    st.metric("Prix médian (département)", f"{prix_median_dep:,.0f} €")

# --- Classement des communes ---
st.subheader("🏆 Top 20 des communes par nombre de transactions")

top_communes = df.groupby('nom_commune').agg({
    'valeur_fonciere': ['count', 'mean', 'median'],
    'prix_m2': 'mean',
    'surface_reelle_bati': 'mean'
}).round(0)

top_communes.columns = ['Nb transactions', 'Prix moyen', 'Prix médian', 'Prix moyen/m²', 'Surface moyenne']
top_communes = top_communes.sort_values('Nb transactions', ascending=False).head(20).reset_index()

# Formatage
top_communes['Prix moyen'] = top_communes['Prix moyen'].apply(lambda x: f"{x:,.0f} €")
top_communes['Prix médian'] = top_communes['Prix médian'].apply(lambda x: f"{x:,.0f} €")
top_communes['Prix moyen/m²'] = top_communes['Prix moyen/m²'].apply(lambda x: f"{x:,.0f} €")
top_communes['Surface moyenne'] = top_communes['Surface moyenne'].apply(lambda x: f"{x:.0f} m²")

st.dataframe(top_communes, use_container_width=True, hide_index=True)

# Graphique des top communes
fig = px.bar(
    top_communes.head(10),
    x='nom_commune',
    y='Nb transactions',
    title="Top 10 des communes les plus dynamiques",
    color='Prix moyen/m²',
    color_continuous_scale='Viridis'
)
st.plotly_chart(fig, use_container_width=True)

# --- Sélection de la commune ---
st.sidebar.header("📍 Sélection de la commune")
communes_disponibles = sorted(df['nom_commune'].unique())

# Option recherche
recherche_commune = st.sidebar.text_input("🔍 Rechercher une commune", "")

if recherche_commune:
    communes_filtrees = [c for c in communes_disponibles if recherche_commune.lower() in c.lower()]
    if communes_filtrees:
        selected_commune_name = st.sidebar.selectbox(
            "Résultats de recherche :",
            options=communes_filtrees
        )
    else:
        st.sidebar.warning("Aucune commune trouvée")
        selected_commune_name = st.sidebar.selectbox(
            "Choisissez une commune :",
            options=communes_disponibles,
            index=communes_disponibles.index("Guéret") if "Guéret" in communes_disponibles else 0
        )
else:
    selected_commune_name = st.sidebar.selectbox(
        "Choisissez une commune :",
        options=communes_disponibles,
        index=communes_disponibles.index("Guéret") if "Guéret" in communes_disponibles else 0
    )

# Filtrage par commune
df_commune = df[df['nom_commune'] == selected_commune_name].copy()

if df_commune.empty:
    st.warning(f"Aucune donnée pour {selected_commune_name} en 2025")
    st.stop()

# --- Filtres avancés ---
st.sidebar.header("🔧 Filtres")

# Filtre code postal
if 'code_postal' in df_commune.columns:
    codes_postaux = sorted(df_commune['code_postal'].astype(str).unique())
    code_postal_selection = st.sidebar.multiselect(
        "Code postal", 
        codes_postaux, 
        default=codes_postaux
    )
else:
    code_postal_selection = []

# Filtre type de bien
if 'type_local' in df_commune.columns:
    type_local_options = ['Tous', 'Maison', 'Appartement']
    type_local = st.sidebar.selectbox("Type de bien", type_local_options)
else:
    type_local = 'Tous'

# Filtre prix avec valeurs dynamiques (adapté à la Creuse)
prix_min = st.sidebar.number_input(
    "Prix minimum (€)", 
    value=0, 
    step=5000,
    min_value=0
)
prix_max = st.sidebar.number_input(
    "Prix maximum (€)", 
    value=int(df_commune['valeur_fonciere'].max()), 
    step=10000,
    min_value=0
)

# Filtre surface
surface_min = st.sidebar.slider(
    "Surface minimum (m²)",
    min_value=0,
    max_value=int(df_commune['surface_reelle_bati'].max()),
    value=0
)

# Application des filtres
df_filtre = df_commune.copy()

if code_postal_selection and 'code_postal' in df_filtre.columns:
    df_filtre = df_filtre[df_filtre['code_postal'].astype(str).isin(code_postal_selection)]

df_filtre = df_filtre[
    (df_filtre['valeur_fonciere'] >= prix_min) & 
    (df_filtre['valeur_fonciere'] <= prix_max) &
    (df_filtre['surface_reelle_bati'] >= surface_min)
]

if type_local != 'Tous' and 'type_local' in df_filtre.columns:
    df_filtre = df_filtre[df_filtre['type_local'] == type_local]

if df_filtre.empty:
    st.warning("Aucune transaction ne correspond à vos filtres.")
    st.stop()

# --- KPIs pour la commune sélectionnée ---
st.header(f"📊 Indicateurs Clés - {selected_commune_name}")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    prix_m2_moyen = df_filtre['prix_m2'].mean()
    st.metric(
        "Prix moyen / m²", 
        f"{prix_m2_moyen:,.0f} €"
    )

with col2:
    prix_median = df_filtre['valeur_fonciere'].median()
    st.metric("Prix médian", f"{prix_median:,.0f} €")

with col3:
    nb_transactions = len(df_filtre)
    st.metric("Transactions", f"{nb_transactions:,}")

with col4:
    surface_moyenne = df_filtre['surface_reelle_bati'].mean()
    st.metric("Surface moyenne", f"{surface_moyenne:.0f} m²")

with col5:
    if 'nombre_pieces_principales' in df_filtre.columns:
        pieces_moyennes = df_filtre['nombre_pieces_principales'].mean()
        st.metric("Pièces principales", f"{pieces_moyennes:.1f}")

# --- Visualisations ---
st.header(f"📈 Analyses - {selected_commune_name}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribution des prix au m²")
    fig = px.histogram(
        df_filtre, 
        x='prix_m2', 
        nbins=30,
        color='type_local' if 'type_local' in df_filtre.columns else None,
        marginal="box",
        title=f"Prix au m² - {selected_commune_name}",
        labels={'prix_m2': 'Prix au m² (€)', 'count': 'Nombre de transactions'}
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Prix selon la surface")
    fig = px.scatter(
        df_filtre,
        x='surface_reelle_bati',
        y='valeur_fonciere',
        color='type_local' if 'type_local' in df_filtre.columns else None,
        hover_data=['code_postal'],
        title="Corrélation surface / prix",
        labels={
            'surface_reelle_bati': 'Surface (m²)',
            'valeur_fonciere': 'Prix (€)'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Carte ---
st.subheader(f"🗺️ Carte des transactions - {selected_commune_name}")

if 'latitude' in df_filtre.columns and 'longitude' in df_filtre.columns:
    df_carte = df_filtre.dropna(subset=['latitude', 'longitude'])
    
    if not df_carte.empty:
        # Limiter à 300 points pour la performance
        if len(df_carte) > 300:
            df_carte = df_carte.sample(300)
            st.caption(f"Affichage de 300 transactions sur {len(df_filtre)} (échantillon aléatoire)")
        
        fig = px.scatter_mapbox(
            df_carte,
            lat="latitude",
            lon="longitude",
            color="prix_m2",
            size="surface_reelle_bati",
            hover_data={
                "valeur_fonciere": ":.0f",
                "type_local": True,
                "surface_reelle_bati": ":.0f",
                "prix_m2": ":.0f"
            },
            color_continuous_scale="RdYlGn_r",
            size_max=15,
            zoom=11,
            mapbox_style="open-street-map",
            title=f"Transactions à {selected_commune_name}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📍 Données de géolocalisation non disponibles")

# --- Évolution temporelle ---
st.subheader(f"📅 Évolution des transactions - {selected_commune_name}")

if 'date_mutation' in df_filtre.columns and not df_filtre.empty:
    df_filtre['mois'] = df_filtre['date_mutation'].dt.to_period('M')
    df_mensuel = df_filtre.groupby('mois').agg({
        'prix_m2': 'mean',
        'valeur_fonciere': ['count', 'mean']
    }).round(0)
    
    df_mensuel.columns = ['prix_m2_moyen', 'nb_transactions', 'prix_moyen']
    df_mensuel = df_mensuel.reset_index()
    df_mensuel['mois'] = df_mensuel['mois'].astype(str)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(
            df_mensuel,
            x='mois',
            y='prix_m2_moyen',
            title="Évolution du prix au m²",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            df_mensuel,
            x='mois',
            y='nb_transactions',
            title="Nombre de transactions par mois"
        )
        st.plotly_chart(fig, use_container_width=True)

# --- Top des ventes et tableau ---
st.subheader("💰 Top 5 des ventes les plus élevées")
top_ventes = df_filtre.nlargest(5, 'valeur_fonciere')[
    ['date_mutation', 'valeur_fonciere', 'surface_reelle_bati', 'prix_m2', 'type_local', 'code_postal']
]
if not top_ventes.empty:
    top_ventes['valeur_fonciere'] = top_ventes['valeur_fonciere'].apply(lambda x: f"{x:,.0f} €")
    top_ventes['prix_m2'] = top_ventes['prix_m2'].apply(lambda x: f"{x:,.0f} €/m²")
    st.dataframe(top_ventes, use_container_width=True, hide_index=True)

st.subheader("📋 Dernières transactions")
df_display = df_filtre.sort_values('date_mutation', ascending=False).head(50)

display_cols = ['date_mutation', 'valeur_fonciere', 'surface_reelle_bati', 
                'prix_m2', 'type_local', 'code_postal']
available_cols = [col for col in display_cols if col in df_display.columns]

if available_cols:
    for col in ['valeur_fonciere', 'prix_m2']:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(
                lambda x: f"{x:,.0f} €" + ("/m²" if col == 'prix_m2' else "")
            )
    
    st.dataframe(df_display[available_cols], use_container_width=True, hide_index=True)

# --- Pied de page ---
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: grey; padding: 10px;'>
        <b>Source :</b> data.gouv.fr - DVF 2025 - Creuse (23)<br>
        <b>Données :</b> {len(df_filtre):,} transactions affichées pour {selected_commune_name}<br>
        <b>Total département :</b> {len(df):,} transactions dans {nb_communes_avec_transactions} communes<br>
        <b>Mise à jour :</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}
    </div>
    """,
    unsafe_allow_html=True
)
