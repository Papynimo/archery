import streamlit as st
from spine_calculator import spine_dynamique_requise

st.set_page_config(page_title="Calculateur de spine", layout="centered")
st.title("🎯 Calculateur de spine pour le tir à l'arc")

st.markdown("Remplissez les paramètres ci-dessous pour obtenir une recommandation de spine statique selon la norme ATA.")

# Champs avec ajustements de granularité
draw_length = st.number_input("Allonge (en pouces)", min_value=0.0, max_value=35.0, value=28.0, step=0.25, format="%.2f")
draw_weight = st.number_input("Puissance à l'allonge (en livres)", min_value=0, max_value=100, value=40, step=1, format="%d")

# Choix du poids de la pointe en grains
grains = st.selectbox("Poids de la pointe (en grains)", options=[50, 75, 100, 125, 150, 175, 200], index=2)
tip_weight = round(grains / 15.4324)  # conversion en grammes pour calcul

# Diamètre de flèche
diameter = st.selectbox(
    "Diamètre de la flèche (en pouces)",
    options=["5/16", "11/32", "non spécifié"],
    index=2,
    help="Le diamètre influence légèrement la rigidité réelle.\n- 5/16\" → plus souple\n- 11/32\" → plus rigide"
)

# Correction liée au diamètre
if diameter == "5/16":
    diameter_offset = -2
elif diameter == "11/32":
    diameter_offset = 2
else:
    diameter_offset = 0

string_type = st.selectbox(
    "Type de corde",
    ["modern", "dacron", "non spécifié"],
    index=2,
    help="Ce champ dépend du matériau, pas de la forme.\nPar ex. :\n- Dacron = 'dacron'\n- Fast Flight, 8125, etc. = 'modern'\nNote : une corde flamande peut être 'modern' ou 'dacron' selon son matériau."
)

silencer_type = st.selectbox("Type de silencieux", ["heavy", "light", "non spécifié"], index=2)
window_cut = st.number_input("Décalage de la fenêtre (center-cut) en mm", min_value=-10, max_value=20, value=0, step=1, format="%d")

# Nettoyage des entrées texte
string_val = string_type if string_type in ["modern", "dacron"] else None
silencer_val = silencer_type if silencer_type in ["heavy", "light"] else None

# Affichage des valeurs saisies
st.write("### Paramètres saisis :")
st.write(f"- Allonge : {draw_length:.2f} pouces")
st.write(f"- Puissance : {draw_weight} livres")
st.write(f"- Pointe : {grains} grains ≈ {tip_weight} g")
st.write(f"- Type de corde : {string_val or 'non spécifié'}")
st.write(f"- Silencieux : {silencer_val or 'non spécifié'}")
st.write(f"- Décalage fenêtre : {window_cut} mm")
st.write(f"- Diamètre flèche : {diameter}")

# Calcul et affichage
if draw_length > 0 and draw_weight > 0:
    result = spine_dynamique_requise(
        W_usine=draw_weight + diameter_offset,
        L_archer=draw_length,
        tip_weight_g=tip_weight,
        string_type=string_val,
        silencer_type=silencer_val,
        window_position_mm=window_cut
    )

    st.markdown("## 📊 Résultats")
    st.success(f"**Spine statique recommandé (ATA)** : `{result['spine_stat_ata']} millièmes de pouce`")
    st.info(f"**Charge dynamique estimée** : `{result['D_dynamic_lb']} lb`")

    with st.expander("🔍 Détails des corrections appliquées"):
        offsets = result['offsets']
        st.write(f"- Correction pointe : {offsets['tip_offset_lb']} lb")
        st.write(f"- Corde : {offsets['string_offset_lb']} lb")
        st.write(f"- Silencieux : {offsets['silencer_offset_lb']} lb")
        st.write(f"- Découpe latérale : {offsets['centercut_offset_lb']} lb")
        st.write(f"- Diamètre flèche : {diameter_offset} lb")
else:
    st.warning("Veuillez saisir une allonge et une puissance supérieures à 0 pour lancer le calcul.")
