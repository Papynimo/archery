import streamlit as st
from spine_calculator import spine_dynamique_requise
from fpdf import FPDF
import datetime
import base64

st.set_page_config(page_title="Calculateur de spine", layout="centered")
st.title("🎯 Calculateur de spine pour le tir à l'arc")

st.markdown("Remplissez les paramètres ci-dessous pour obtenir une recommandation de spine statique selon la norme ATA.")

draw_length = st.number_input("Allonge (en pouces)", min_value=0.0, max_value=35.0, value=28.0, step=0.25, format="%.2f")
draw_weight = st.number_input("Puissance à l'allonge (en livres)", min_value=0, max_value=100, value=40, step=1, format="%d")

grains = st.selectbox("Poids de la pointe (en grains)", options=[50, 75, 100, 125, 150, 175, 200], index=2)
tip_weight = round(grains / 15.4324)

diameter = st.selectbox(
    "Diamètre de la flèche (en pouces)",
    options=["5/16", "11/32", "non spécifié"],
    index=2,
    help="Le diamètre influence légèrement la rigidité réelle.\n- 5/16\" → plus souple\n- 11/32\" → plus rigide"
)

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

string_val = string_type if string_type in ["modern", "dacron"] else None
silencer_val = silencer_type if silencer_type in ["heavy", "light"] else None

st.write("### Paramètres saisis :")
st.write(f"- Allonge : {draw_length:.2f} pouces")
st.write(f"- Puissance : {draw_weight} livres")
st.write(f"- Pointe : {grains} grains ≈ {tip_weight} g")
st.write(f"- Type de corde : {string_val or 'non spécifié'}")
st.write(f"- Silencieux : {silencer_val or 'non spécifié'}")
st.write(f"- Décalage fenêtre : {window_cut} mm")
st.write(f"- Diamètre flèche : {diameter}")

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

    # Bouton pour générer le PDF
    if st.button("📄 Générer un rapport PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Rapport de Calcul de Spine - Tir à l'arc", ln=True, align='C')
        pdf.ln(10)

        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.cell(200, 10, txt=f"Date : {date_str}", ln=True)
        pdf.ln(5)

        pdf.cell(200, 10, txt="Paramètres saisis :", ln=True)
        pdf.cell(200, 8, txt=f"Allonge : {draw_length} pouces", ln=True)
        pdf.cell(200, 8, txt=f"Puissance : {draw_weight} lbs", ln=True)
        pdf.cell(200, 8, txt=f"Pointe : {grains} grains ≈ {tip_weight} g", ln=True)
        pdf.cell(200, 8, txt=f"Type de corde : {string_val or 'non spécifié'}", ln=True)
        pdf.cell(200, 8, txt=f"Silencieux : {silencer_val or 'non spécifié'}", ln=True)
        pdf.cell(200, 8, txt=f"Décalage fenêtre : {window_cut} mm", ln=True)
        pdf.cell(200, 8, txt=f"Diamètre flèche : {diameter}", ln=True)
        pdf.ln(5)

        pdf.cell(200, 10, txt="Résultats :", ln=True)
        pdf.cell(200, 8, txt=f"Spine statique recommandé : {result['spine_stat_ata']} millièmes de pouce", ln=True)
        pdf.cell(200, 8, txt=f"Charge dynamique estimée : {result['D_dynamic_lb']} lb", ln=True)
        pdf.ln(5)

        pdf.cell(200, 10, txt="Corrections appliquées :", ln=True)
        for k, v in offsets.items():
            pdf.cell(200, 8, txt=f"{k.replace('_', ' ')} : {v} lb", ln=True)
        pdf.cell(200, 8, txt=f"Correction diamètre : {diameter_offset} lb", ln=True)

        # Enregistrement temporaire
        pdf_path = "/tmp/rapport_spine.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="rapport_spine.pdf">📥 Télécharger le rapport PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Veuillez saisir une allonge et une puissance supérieures à 0 pour lancer le calcul.")
