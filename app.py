import streamlit as st
import pandas as pd

# Configuration globale
st.set_page_config(page_title="Mon Séjour à Oslo", page_icon="🇳🇴", layout="wide")

st.title("🇳🇴 Carnet de Voyage : Oslo")
st.caption("Du 15 au 19 octobre")

# Taux de conversion indicatif (1 NOK ≈ 0.088 EUR)
NOK_TO_EUR = 0.088

# ---------------------------------------------------------
# DONNÉES
# ---------------------------------------------------------
itinerary_data = [
    {"Jour": "J1 - 15/10", "Heure": "Après-midi", "Lieu": "Opéra d'Oslo", "Type": "Culture", "lat": 59.9075, "lon": 10.7531, "Description": "Promenade sur le toit en marbre pour la vue sur le fjord."},
    {"Jour": "J1 - 15/10", "Heure": "Fin d'aprem", "Lieu": "Quartier Bjørvika & MUNCH", "Type": "Culture", "lat": 59.9053, "lon": 10.7553, "Description": "Visite du musée MUNCH et découverte de l'architecture moderne."},
    {"Jour": "J2 - 16/10", "Heure": "Matin", "Lieu": "Parc Vigeland", "Type": "Parc", "lat": 59.9270, "lon": 10.7008, "Description": "Exploration du parc de sculptures impressionnant de Gustav Vigeland."},
    {"Jour": "J2 - 16/10", "Heure": "Après-midi", "Lieu": "Presqu'île de Bygdøy", "Type": "Musée", "lat": 59.9028, "lon": 10.6840, "Description": "Musée Fram (exploration polaire) et musée Kon-Tiki."},
    {"Jour": "J3 - 17/10", "Heure": "Matin", "Lieu": "Palais Royal & Karl Johans gate", "Type": "Balade", "lat": 59.9169, "lon": 10.7275, "Description": "Relève de la garde à 13h30 et descente de l'artère principale."},
    {"Jour": "J3 - 17/10", "Heure": "Après-midi", "Lieu": "Musée National (Nasjonalmuseet)", "Type": "Culture", "lat": 59.9130, "lon": 10.7330, "Description": "Le plus grand musée d'art des pays nordiques."},
    {"Jour": "J3 - 17/10", "Heure": "Soir", "Lieu": "Aker Brygge & Tjuvholmen", "Type": "Dîner", "lat": 59.9100, "lon": 10.7250, "Description": "Promenade le long du quai et dîner au bord de l'eau."},
    {"Jour": "J4 - 18/10", "Heure": "Matin", "Lieu": "Quartier Grünerløkka", "Type": "Shopping/Café", "lat": 59.9228, "lon": 10.7589, "Description": "Ambiance vintage, boutiques de créateurs et cafés indépendants."},
    {"Jour": "J4 - 18/10", "Heure": "Après-midi", "Lieu": "Balade le long d'Akerselva", "Type": "Nature", "lat": 59.9260, "lon": 10.7520, "Description": "Randonnée urbaine le long de la rivière jusqu'à Mathallen."},
    {"Jour": "J5 - 19/10", "Heure": "Matin", "Lieu": "Saut à ski de Holmenkollen", "Type": "Vue", "lat": 59.9639, "lon": 10.6661, "Description": "Accès en métro T-Bane. Vue panoramique spectaculaire sur tout le fjord."},
]

df_itinerary = pd.DataFrame(itinerary_data)

# Initialisation du budget en session_state pour pouvoir ajouter/supprimer des dépenses
if "expenses" not in st.session_state:
    st.session_state.expenses = [
        {"Poste": "Vol A/R", "Montant_NOK": 1800, "Catégorie": "Transport"},
        {"Poste": "Hôtel (4 nuits)", "Montant_NOK": 5500, "Catégorie": "Hébergement"},
        {"Poste": "Oslo Pass 72h", "Montant_NOK": 820, "Catégorie": "Activités"},
    ]

# ---------------------------------------------------------
# NAVIGATION PAR ONGLETS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗓️ Parcours", 
    "💶 Budget", 
    "🚆 Transports", 
    "🌤️ Météo (Octobre)", 
    "☕ Restaurants & Cafés"
])

# --- TAB 1: PARCOURS & CARTE ---
with tab1:
    st.header("Planning jour par jour & Carte")
    
    col_nav, col_map = st.columns([1, 1])
    
    with col_nav:
        jour_selectionne = st.selectbox("Choisir la journée :", df_itinerary["Jour"].unique())
        df_jour = df_itinerary[df_itinerary["Jour"] == jour_selectionne]
        
        for _, row in df_jour.iterrows():
            with st.expander(f"{row['Heure']} : **{row['Lieu']}** ({row['Type']})", expanded=True):
                st.write(row["Description"])

    with col_map:
        st.subheader("Carte de la journée")
        st.map(df_jour[["lat", "lon"]], zoom=12)

# --- TAB 2: BUDGET ---
with tab2:
    st.header("💳 Gestionnaire de Budget")
    
    # Formulaire d'ajout rapide
    with st.form("add_expense"):
        col_name, col_amount, col_cat, col_btn = st.columns([3, 2, 2, 2])
        poste = col_name.text_input("Intitulé", placeholder="ex: Café & Cinnamon Roll")
        montant_nok = col_amount.number_input("Montant (NOK)", min_value=0.0, step=10.0)
        cat = col_cat.selectbox("Catégorie", ["Repas", "Transport", "Activités", "Hébergement", "Divers"])
        submitted = col_btn.form_submit_button("Ajouter")
        
        if submitted and poste and montant_nok > 0:
            st.session_state.expenses.append({"Poste": poste, "Montant_NOK": montant_nok, "Catégorie": cat})
            st.rerun()

    # Affichage du tableau et des totaux
    df_exp = pd.DataFrame(st.session_state.expenses)
    if not df_exp.empty:
        df_exp["Montant_EUR"] = (df_exp["Montant_NOK"] * NOK_TO_EUR).round(2)
        
        st.dataframe(df_exp, use_container_width=True)
        
        total_nok = df_exp["Montant_NOK"].sum()
        total_eur = df_exp["Montant_EUR"].sum()
        
        col_t1, col_t2 = st.columns(2)
        col_t1.metric("Total Dépensé (NOK)", f"{total_nok:,.0f} NOK")
        col_t2.metric("Total Dépensé (EUR)", f"{total_eur:,.2f} €")

# --- TAB 3: TRANSPORTS ---
with tab3:
    st.header("🚍 Se déplacer à Oslo")
    
    st.info("💡 **Astuce réseau :** Tous les bus, trams, métros (T-bane) et ferries municipaux dépendent du réseau unique **Ruter**.")
    
    col_tr1, col_tr2 = st.columns(2)
    
    with col_tr1:
        st.subheader("✈️ Transfert Aéroport (Gardermoen - OSL)")
        st.markdown("""
        * **Train Régional Vy (Recommandé) :** 
          * *Prix :* ~118 NOK (~10,50 €)
          * *Durée :* 23 min jusqu'à Oslo S (Gare centrale).
          * *Inclus dans l'Oslo Pass.*
        * **Flytoget (Train Express Airport) :**
          * *Prix :* ~230 NOK (~20 €)
          * *Durée :* 19 min (Départs toutes les 10 min).
        """)
        
    with col_tr2:
        st.subheader("🎟️ Titres de Transport (Ruter / Oslo Pass)")
        st.markdown("""
        * **Ticket à l'unité (Zone 1) :** ~42 NOK (~3,70 €) — valable 60 min.
        * **Pass 24h Ruter :** ~127 NOK (~11 €).
        * **Oslo Pass (24h / 48h / 72h) :**
          * Accès illimité aux transports (zones 1 & 2).
          * Entrée gratuite dans plus de 30 musées (MUNCH, Fram, Musée National, etc.).
          * Téléchargeable directement sur l'application mobile *Oslo Pass*.
        """)

# --- TAB 4: MÉTÉO DE MI-OCTOBRE ---
with tab4:
    st.header("🌤️ Climat & Météo moyenne (15 - 19 Octobre)")
    
    st.warning("🍂 En mi-octobre à Oslo, l'automne est bien installé. Les journées sont fraîches et humides.")
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Température Max (Jour)", "7°C - 9°C")
    col_m2.metric("Température Min (Nuit)", "2°C - 4°C")
    col_m3.metric("Humidité / Pluie", "~80% (Pluie possible)")
    
    st.subheader("🎒 Recommandations d'équipement")
    st.markdown("""
    - **Système des 3 couches :** T-shirt respirant, pull chaud (laine ou polaire), et veste imperméable/coupe-vent.
    - **Chaussures :** Bonnes chaussures de marche imperméables (trottoirs ou sentiers mouillés).
    - **Accessoires :** Bonnet léger, écharpe et parapluie compact.
    - **Luminosité :** Le soleil se couche vers 18h00 mi-octobre. Profite des matinées !
    """)

# --- TAB 5: RESTAURANTS & CAFÉS ---
with tab5:
    st.header("☕ Adresses Gourmandes")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.subheader("☕ Cafés & Pauses Fika")
        st.markdown("""
        * **Tim Wendelboe** *(Grünerløkka)* : Micro-torréfacteur de renommée mondiale.
        * **Fuglen** *(Centre)* : Café le jour, bar à cocktails rétro la nuit.
        * **W.B. Samson** : La plus ancienne boulangerie d'Oslo (*kanelboller* à goûter absolument).
        """)
        
    with col_c2:
        st.subheader("🍽️ Food Courts & Restaurants")
        st.markdown("""
        * **Mathallen Oslo** *(Vulkan)* : Halle gourmande avec stands de spécialités norvégiennes.
        * **VIA Village** *(Vika)* : Food court moderne et convivial.
        * **Fiskeriet Youngstorget** : Idéal pour déguster une soupe de poisson traditionnelle (*fiskesuppe*).
        """)