import streamlit as st
from spine_calculator import spine_dynamique_requise
from fpdf import FPDF
import datetime
import base64

# Classe PDF simplifiée sans set_font dans header
class PDF(FPDF):
    def header(self):
        self.cell(200, 10, "Rapport de Calcul de Spine - Tir à l'arc", ln=True, align='C')
        self.ln(10)

st.set_page_config(page_title="Calculateur de spine", layout="centered")
st.title("🎯 Calculateur de spine pour le tir à l'arc")

draw_length = st.number_input("Allonge (en pouces)", min_value=0.0, max_value=35.0, value=28.0, step=0.25, format="%.2f")
draw_weight = st.number_input("Puissance à l'allonge (en livres)", min_value=0, max_value=100, value=40, step=1, format="%d")
grains = st.selectbox("Poids de la pointe (en grains)", options=[50, 75, 100, 125, 150, 175, 200], index=2)
tip_weight = round(grains / 15.4324)

diameter = st.selectbox("Diamètre de la flèche (en pouces)", ["5/16", "11/32", "non spécifié"], index=2)
diameter_offset = -2 if diameter == "5/16" else 2 if diameter == "11/32" else 0

string_type = st.selectbox("Type de corde", ["modern", "dacron", "non spécifié"], index=2)
silencer_type = st.selectbox("Type de silencieux", ["heavy", "light", "non spécifié"], index=2)
window_cut = st.number_input("Décalage de la fenêtre (center-cut) en mm", min_value=-10, max_value=20, value=0, step=1, format="%d")

string_val = string_type if string_type in ["modern", "dacron"] else None
silencer_val = silencer_type if silencer_type in ["heavy", "light"] else None

if draw_length > 0 and draw_weight > 0:
    result = spine_dynamique_requise(
        W_usine=draw_weight + diameter_offset,
        L_archer=draw_length,
        tip_weight_g=tip_weight,
        string_type=string_val,
        silencer_type=silencer_val,
        window_position_mm=window_cut
    )

    st.success(f"Spine recommandé : {result['spine_stat_ata']} millièmes de pouce")
    st.info(f"Charge dynamique estimée : {result['D_dynamic_lb']} lb")

    if st.button("📄 Générer un rapport PDF"):
        pdf = PDF()
        pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        pdf.set_font("DejaVu", size=12)
        pdf.add_page()

        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.cell(200, 10, f"Date : {date_str}", ln=True)
        pdf.cell(200, 8, f"Allonge : {draw_length} pouces", ln=True)
        pdf.cell(200, 8, f"Puissance : {draw_weight} lbs", ln=True)
        pdf.cell(200, 8, f"Pointe : {grains} grains (env. {tip_weight} g)", ln=True)
        pdf.cell(200, 8, f"Type de corde : {string_val or 'non spécifié'}", ln=True)
        pdf.cell(200, 8, f"Silencieux : {silencer_val or 'non spécifié'}", ln=True)
        pdf.cell(200, 8, f"Décalage fenêtre : {window_cut} mm", ln=True)
        pdf.cell(200, 8, f"Diamètre flèche : {diameter}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 8, f"Spine statique recommandé : {result['spine_stat_ata']} millièmes de pouce", ln=True)
        pdf.cell(200, 8, f"Charge dynamique estimée : {result['D_dynamic_lb']} lb", ln=True)

        offsets = result['offsets']
        pdf.ln(5)
        pdf.cell(200, 10, "Corrections appliquées :", ln=True)
        for k, v in offsets.items():
            pdf.cell(200, 8, f"{k.replace('_', ' ')} : {v} lb", ln=True)
        pdf.cell(200, 8, f"Correction diamètre : {diameter_offset} lb", ln=True)

        pdf_path = "/tmp/rapport_spine.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            href = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="rapport_spine.pdf">📥 Télécharger le rapport PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("Veuillez saisir une allonge et une puissance valides.")


