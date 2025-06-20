import streamlit as st
from spine_calculator import spine_dynamique_requise

st.set_page_config(
    page_title="Calculateur de Spine Dynamique",
    layout="centered"
)

st.title("🎯 Calculateur de Spine Dynamique pour Flèches en Bois")

st.sidebar.header("Paramètres de l'arc et de l'archer")
W_usine = st.sidebar.number_input("Poids d'armement à la longueur usine (lb)", 0.0, 100.0, 50.0, 1.0)
L_archer = st.sidebar.number_input("Allonge de l'archer (inch)", 0.0, 36.0, 29.0, 0.5)

st.sidebar.header("Paramètres additionnels")
tip_weight_g = st.sidebar.number_input("Poids de la pointe (g)", 0.0, 100.0, 11.0, 1.0)
string_type = st.sidebar.selectbox("Type de corde", ['none','modern','dacron'])
silencer_type = st.sidebar.selectbox("Type de silencieux", ['none','light','heavy'])
window_position_mm = st.sidebar.number_input("Position de la fenêtre (mm)", 0.0, 10.0, 2.0, 0.5)

if st.sidebar.button("Calculer"):
    s_type = None if string_type=='none' else string_type
    sil_type = None if silencer_type=='none' else silencer_type
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
    st.markdown("**Offsets appliqués (lb)** :")
    st.json(result['offsets'])
