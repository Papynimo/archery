"""
streamlit_app.py

Application Streamlit pour calculer la spine dynamique des flèches en bois.
"""
import streamlit as st
from spine_calculator import spine_dynamique_requise

st.set_page_config(
    page_title="Calculateur de Spine Dynamique",
    layout="centered"
)

st.title("🎯 Calculateur de Spine Dynamique pour Flèches en Bois")

st.sidebar.header("Paramètres de l'arc et de l'archer")
W_usine = st.sidebar.number_input(
    "Poids d'armement à la longueur usine (lb)",
    min_value=0.0, value=50.0, step=1.0
)
L_archer = st.sidebar.number_input(
    "Allonge de l'archer (inch)",
    min_value=0.0, value=29.0, step=0.5
)

st.sidebar.header("Paramètres additionnels")
tip_weight_g = st.sidebar.number_input(
    "Poids de la pointe (g)",
    min_value=0.0, value=11.0, step=1.0
)
string_type = st.sidebar.selectbox(
    "Type de corde",
    ['none', 'modern', 'dacron']
)
silencer_type = st.sidebar.selectbox(
    "Type de silencieux",
    ['none', 'light', 'heavy']
)
window_position_mm = st.sidebar.number_input(
    "Position de la fenêtre (centre-cut) en mm",
    min_value=0.0, value=2.0, step=0.5
)

if st.sidebar.button("Calculer"):
    # Convertir 'none' en None pour la fonction
    s_type = None if string_type == 'none' else string_type
    sil_type = None if silencer_type == 'none' else silencer_type

    # Appel de la fonction de calcul
    result = spine_dynamique_requise(
        W_usine=W_usine,
        L_archer=L_archer,
        tip_weight_g=tip_weight_g,
        string_type=s_type,
        silencer_type=sil_type,
        window_position_mm=window_position_mm
    )

    st.subheader("Résultats")
    st.write(f"**Charge dynamique cible** : {result['D_dynamic_lb']:.1f} lb")
    st.write(f"**Spine statique recommandée** : {result['spine_stat_ata']:.0f} millièmes de pouce")
    st.markdown("**Détail des offsets appliqués (en lb)** :")
    st.json(result['offsets'])

    st.markdown("---")
    st.write(
        "🔧 Ajuste les paramètres dans la barre latérale pour voir "
        "leur impact en temps réel sur la charge dynamique et la spine."
    )

