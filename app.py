import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from collections import Counter
import re

# Configuration de la page
st.set_page_config(
    page_title="Données nationales sur les offres d'emploi au Sénégal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé avec la palette de couleurs
st.markdown("""
<style>
    .main {
        background-color: #F8F9FA;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #007BFF;
        color: white;
        border-radius: 5px 5px 0px 0px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #28A745;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 5px solid #007BFF;
    }
    .sidebar .sidebar-content {
        background-color: #E5E5E5;
    }
    h1 {
        color: #007BFF;
        text-align: center;
        padding: 20px 0;
    }
    h2, h3 {
        color: #212529;
    }
    .stButton > button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('df_scrapped_complet.csv')
        # Conversion de la date
        df['Date_publication'] = pd.to_datetime(df['Date_publication'], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Fichier 'df_scrapped_complet.csv' non trouvé. Veuillez vous assurer que le fichier est dans le bon répertoire.")
        return pd.DataFrame()

# Fonction pour calculer les catégories de dates
def categorize_date(date):
    if pd.isna(date):
        return "Date inconnue"
    
    now = datetime.now()
    diff = (now - date).days
    
    if diff <= 1:
        return "Aujourd'hui"
    elif diff <= 7:
        return "Moins de 7 jours"
    elif diff <= 10:
        return "Moins de 10 jours"
    elif diff <= 30:
        return "Moins de 30 jours"
    elif diff <= 90:
        return "Moins de 3 mois"
    elif diff <= 180:
        return "Moins de 6 mois"
    else:
        return "Plus de 6 mois"

# Fonction pour extraire les compétences
def extract_competences(competences_str):
    if pd.isna(competences_str):
        return []
    # Diviser par des séparateurs communs et nettoyer
    competences = re.split(r'[,;|\n]+', str(competences_str))
    return [comp.strip().lower() for comp in competences if comp.strip()]

# Titre principal
st.markdown("# Données nationales sur les offres d'emploi au Sénégal")

# Chargement des données
df = load_data()

if df.empty:
    st.stop()

# Préparation des données
df['Categorie_date'] = df['Date_publication'].apply(categorize_date)

# Création des onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Accueil", "👥 À propos", "💼 Offres d'emploi", "📈 Tableau de bord", "❓ Aide"])


# ONGLET ACCUEIL
with tab1:
    st.markdown("## Bienvenue sur le tableau de bord des offres d'emploi au Sénégal")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #007BFF; margin: 0;">📋 Total des offres</h3>
            <h2 style="margin: 10px 0; color: #212529;">{len(df):,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        secteurs_uniques = df['secteur'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #28A745; margin: 0;">🏢 Secteurs actifs</h3>
            <h2 style="margin: 10px 0; color: #212529;">{secteurs_uniques}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        lieux_uniques = df['Lieu'].nunique()
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #FFA500; margin: 0;">📍 Villes</h3>
            <h2 style="margin: 10px 0; color: #212529;">{lieux_uniques}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        offres_recentes = len(df[df['Categorie_date'].isin(['Aujourd\'hui', 'Moins de 7 jours'])])
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="color: #1E90FF; margin: 0;">🔥 Offres récentes</h3>
            <h2 style="margin: 10px 0; color: #212529;">{offres_recentes}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Informations clés")
        st.markdown("""
        - **Analyse** des offres d'emploi au Sénégal
        - **Identification des compétences** les plus demandées
        - **Suivi des secteurs** qui recrutent le plus
        - **Filtrage avancé** par lieu, secteur, type de contrat
        - **Visualisations interactives** pour une meilleure compréhension
        """)
    
    with col2:
        st.markdown("### Objectifs")
        st.markdown("""
        Cette plateforme vous permet de :
        - Découvrir les tendances du marché de l'emploi
        - Identifier les opportunités par secteur
        - Analyser la répartition géographique des offres
        - Comprendre les exigences en compétences
        - Suivre l'évolution temporelle des recrutements
        """)

# ONGLET À PROPOS
with tab2:
    st.markdown("## À propos des auteurs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎓 CAMARA Sanor
        **Étudiant en dernière année à l'ENSAE**
        
        Passionné par l'analyse de données et les statistiques appliquées au marché de l'emploi.
        Spécialisé dans la visualisation de données et l'analyse économique.
        """)
    
    with col2:
        st.markdown("""
        ### 🎓 Kebjam Jackson
        **Étudiant en dernière année à l'ENSAE**
        
        Expert en développement d'applications d'analyse de données et en intelligence économique.
        Spécialisé dans les technologies de traitement de données massives.
        """)
    
    st.markdown("---")
    st.markdown("""
    ### À propos de l'ENSAE
    L'École Nationale de la Statistique et de l'Analyse Économique (ENSAE) forme des cadres supérieurs 
    en statistique, économie et analyse de données. Ce projet s'inscrit dans le cadre de nos études 
    et vise à apporter une contribution significative à l'analyse du marché de l'emploi au Sénégal.
    
    ### Mission du projet
    Fournir aux chercheurs d'emploi, aux entreprises et aux décideurs politiques des insights 
    précieux sur les tendances du marché de l'emploi sénégalais grâce à l'analyse de données.
    """)

# ONGLET OFFRES D'EMPLOI
with tab3:
    st.markdown("## 💼 Offres d'emploi par secteur")
    
    # Filtres
    col1, col2 = st.columns(2)
    with col1:
        secteur_filtre = st.selectbox("Filtrer par secteur", ["Tous"] + sorted(df['secteur'].dropna().unique().tolist()))
    with col2:
        date_filtre = st.selectbox("Filtrer par ancienneté", ["Toutes"] + sorted(df['Categorie_date'].unique().tolist()))
    
    # Application des filtres
    df_filtre = df.copy()
    if secteur_filtre != "Tous":
        df_filtre = df_filtre[df_filtre['secteur'] == secteur_filtre]
    if date_filtre != "Toutes":
        df_filtre = df_filtre[df_filtre['Categorie_date'] == date_filtre]
    
    # Tri par date (plus récent en premier)
    df_filtre = df_filtre.sort_values('Date_publication', ascending=False, na_position='last')
    
    # Groupement par secteur
    secteurs_grouped = df_filtre.groupby('secteur').size().sort_values(ascending=False)
    
    # Graphique des secteurs
    fig_secteur = px.bar(
        x=secteurs_grouped.values,
        y=secteurs_grouped.index,
        orientation='h',
        title=f"Nombre d'offres par secteur ({len(df_filtre)} offres)",
        color=secteurs_grouped.values,
        color_continuous_scale="Blues"
    )
    fig_secteur.update_layout(
        xaxis_title="Nombre d'offres",
        yaxis_title="Secteur",
        height=600
    )
    st.plotly_chart(fig_secteur, use_container_width=True)
    
    # Tableau des offres
    st.markdown("### Liste détaillée des offres")
    
    # Colonnes à afficher
    colonnes_affichage = ['Titre_poste', 'Lieu', 'secteur', 'Type_contrat', 'Date_publication', 'Categorie_date']
    df_affichage = df_filtre[colonnes_affichage].copy()
    
    # Formatage de la date
    df_affichage['Date_publication'] = df_affichage['Date_publication'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(
        df_affichage,
        use_container_width=True,
        height=400,
        hide_index=True
    )

# ONGLET DASHBOARD



with tab4:
    st.markdown("## Dashboard analytique")
    
    # Sidebar pour les filtres
    with st.sidebar:
        st.markdown("### Filtres pour tableau de bord")
        
        # Filtres multiples
        secteurs_selectionnes = st.multiselect(
            "Secteurs",
            options=sorted(df['secteur'].dropna().unique()),
            default=[]
        )
        
        lieux_selectionnes = st.multiselect(
            "Lieux",
            options=sorted(df['Lieu'].dropna().unique()),
            default=[]
        )
        
        types_contrat_selectionnes = st.multiselect(
            "Types de contrat",
            options=sorted(df['Type_contrat_regroupe'].dropna().unique()),
            default=[]
        )
        
        date_categories = st.multiselect(
            "Ancienneté des offres",
            options=sorted(df['Categorie_date'].unique()),
            default=[]
        )
    
    # Application des filtres
    df_dashboard = df.copy()
    
    if secteurs_selectionnes:
        df_dashboard = df_dashboard[df_dashboard['secteur'].isin(secteurs_selectionnes)]
    if lieux_selectionnes:
        df_dashboard = df_dashboard[df_dashboard['Lieu'].isin(lieux_selectionnes)]
    if types_contrat_selectionnes:
        df_dashboard = df_dashboard[df_dashboard['Type_contrat_regroupe'].isin(types_contrat_selectionnes)]
    if date_categories:
        df_dashboard = df_dashboard[df_dashboard['Categorie_date'].isin(date_categories)]

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Offres filtrées", len(df_dashboard))
    with col2:
        st.metric("Secteurs actifs", df_dashboard['secteur'].nunique())
    with col3:
        st.metric("Villes concernées", df_dashboard['Lieu'].nunique())
    with col4:
        secteur_top = df_dashboard['secteur'].mode()[0] if not df_dashboard.empty else "0"
        st.metric("Secteur leader", secteur_top)
 
    # Graphiques principaux
    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 des secteurs qui recrutent le plus
        secteurs_top = df_dashboard['secteur'].value_counts().head(10)

        # Création d’un DataFrame pour plotly express
        secteurs_top_df = secteurs_top.reset_index()
        secteurs_top_df.columns = ['Secteur', 'Nombre_offres']

        fig_secteurs = px.bar(
            secteurs_top_df,
            x="Nombre_offres",
            y="Secteur",
            orientation='h',
            title="Top 10 des secteurs qui recrutent le plus",
            color="Nombre_offres",
            color_continuous_scale="Viridis"
        )

        fig_secteurs.update_layout(height=500)
        st.plotly_chart(fig_secteurs, use_container_width=True)

    
    with col2:
        # Répartition par type de contrat
        contrats = df_dashboard['Type_contrat_regroupe'].value_counts().reset_index()
        contrats.columns = ['Type de contrat', 'Nombre']

        fig_contrats = px.pie(
            contrats,
            values='Nombre',
            names='Type de contrat',
            title="Répartition par type de contrat"
        )
        fig_contrats.update_layout(height=500)
        st.plotly_chart(fig_contrats, use_container_width=True)

    # Analyse des compétences
    st.markdown("### Compétences les plus demandées")

    # Extraction et analyse des compétences
    toutes_competences = []
    for comp_str in df_dashboard['competences'].dropna():
        toutes_competences.extend(extract_competences(comp_str))

    if toutes_competences:
        from collections import Counter
        competences_counter = Counter(toutes_competences)
        top_competences = competences_counter.most_common(20)

        comp_df = pd.DataFrame(top_competences, columns=['Compétence', 'Fréquence'])

        fig_comp = px.bar(
            comp_df,
            x='Fréquence',
            y='Compétence',
            orientation='h',
            title="Top 20 des compétences les plus demandées",
            color='Fréquence',
            color_continuous_scale="Blues"
        )
        fig_comp.update_layout(height=700)
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.info("Aucune donnée de compétences disponible pour les filtres sélectionnés.")

    # Analyse temporelle
    col1, col2 = st.columns(2)

    with col1:
        # Distribution par ancienneté
        dates_dist = df_dashboard['Categorie_date'].value_counts().reset_index()
        dates_dist.columns = ['Ancienneté', 'Nombre']

        fig_dates = px.bar(
            dates_dist,
            x='Ancienneté',
            y='Nombre',
            title="Distribution par ancienneté des offres",
            color='Nombre',
            color_continuous_scale="Oranges"
        )
        fig_dates.update_layout(height=500)
        st.plotly_chart(fig_dates, use_container_width=True)

    
    with col2:
        # Top 10 des villes qui recrutent
        villes_top = df_dashboard['Lieu'].value_counts().head(10).reset_index()
        villes_top.columns = ['Ville', 'Nombre_offres']

        fig_villes = px.bar(
            villes_top,
            x='Nombre_offres',
            y='Ville',
            orientation='h',
            title="Top 10 des villes qui recrutent",
            color='Nombre_offres',
            color_continuous_scale="Reds"
        )

        fig_villes.update_layout(height=500)
        st.plotly_chart(fig_villes, use_container_width=True)


# ONGLET AIDE
with tab5:
    st.markdown("## Guide d'utilisation")
    
    st.markdown("""
    ### Comment utiliser cette application
    
    Cette application vous permet d'analyser les offres d'emploi au Sénégal de manière interactive.
    
    ####  **Onglet Accueil**
    - Vue d'ensemble des statistiques principales
    - Métriques clés sur les offres d'emploi
    - Informations générales sur le dataset
    
    #### **Onglet Offres d'emploi**
    - Visualisation des offres groupées par secteur
    - Filtrage par secteur et ancienneté
    - Liste détaillée des offres triées par date
    
    ####  **Onglet Dashboard**
    - Analyses approfondies avec filtres avancés
    - Identification des secteurs qui recrutent le plus
    - Analyse des compétences les plus demandées
    - Visualisations interactives
    
    ###  **Utilisation des filtres**
    
    **Dans la barre latérale (Dashboard) :**
    - **Secteurs** : Sélectionnez un ou plusieurs secteurs d'activité
    - **Lieux** : Filtrez par ville ou région
    - **Types de contrat** : CDI, CDD, Stage, etc.
    - **Ancienneté** : Filtrez par date de publication
    
    **Catégories d'ancienneté :**
    - **Aujourd'hui** : Offres publiées aujourd'hui
    - **Moins de 7 jours** : Offres de la semaine
    - **Moins de 10 jours** : Offres récentes
    - **Moins de 30 jours** : Offres du mois
    - **Moins de 3 mois** : Offres du trimestre
    - **Moins de 6 mois** : Offres du semestre
    - **Plus de 6 mois** : Offres anciennes
    
    ### **Interprétation des graphiques**
    
    #### **Graphiques en barres**
    - Les barres horizontales montrent les classements
    - Les couleurs indiquent l'intensité (plus foncé = plus élevé)
    - Survolez les barres pour voir les valeurs exactes
    
    #### **Graphiques circulaires**
    - Montrent les proportions relatives
    - Cliquez sur les légendes pour masquer/afficher des segments
    
    #### **Graphiques interactifs**
    - Zoom : Double-clic ou molette de la souris
    - Sélection : Cliquez et glissez
    - Reset : Double-clic sur l'arrière-plan
    
    ###  **Conseils d'utilisation**
    
    1. **Commencez par l'accueil** pour avoir une vue d'ensemble
    2. **Utilisez les filtres** pour affiner vos recherches
    3. **Explorez les secteurs** dans l'onglet offres d'emploi
    4. **Analysez les tendances** dans le dashboard
    5. **Exportez les données** en faisant un clic droit sur les tableaux
    
    ###  **Questions fréquentes**
    
    **Q : Comment identifier les compétences les plus demandées ?**
    R : Consultez le graphique "Compétences les plus demandées" dans l'onglet Dashboard.
    
    **Q : Quels sont les secteurs qui recrutent le plus ?**
    R : Utilisez le graphique "Top 10 des secteurs qui recrutent le plus" dans le Dashboard.
    
    **Q : Comment voir uniquement les offres récentes ?**
    R : Filtrez par "Aujourd'hui" ou "Moins de 7 jours" dans les filtres d'ancienneté.
    
    **Q : Les graphiques ne se mettent pas à jour ?**
    R : Vérifiez que vous avez sélectionné au moins une option dans chaque filtre utilisé.
    
    ###  **Support**
    
    Pour toute question ou suggestion d'amélioration, contactez les auteurs :
    - CAMARA Sanor
    - Kebjam Jackson
    
    *Étudiants en dernière année à l'ENSAE*
    """)
    
    # Section technique
    with st.expander("🔧 Informations techniques"):
        st.markdown("""
        **Technologies utilisées :**
        - **Streamlit** : Framework d'application web
        - **Pandas** : Manipulation des données
        - **Plotly** : Visualisations interactives
        - **Python** : Langage de programmation
        
        **Structure des données :**
        - **Titre_poste** : Intitulé du poste
        - **Lieu** : Localisation de l'emploi
        - **Type_contrat** : Type de contrat détaillé
        - **Date_publication** : Date de publication de l'offre
        - **secteur** : Secteur d'activité
        - **competences** : Compétences requises
        - **Type_contrat_regroupe** : Type de contrat simplifié
        
        **Performance :**
        - Mise en cache des données pour une navigation rapide
        - Filtrage optimisé pour de gros volumes de données
        - Interface responsive pour tous les écrans
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6C757D; padding: 20px;'>
    <p> Données nationales sur les offres d'emploi au Sénégal</p>
    <p>Développé par CAMARA Sanor & Kebjam Jackson - ENSAE</p>
    <p>© 2025 - Tous droits réservés</p>
</div>
""", unsafe_allow_html=True)

#if __name__ == "__main__":
#    main()