"""
spine_calculator.py

Module pour calculer la charge dynamique cible et la spine statique recommandée
pour des flèches en bois, selon différents paramètres liés à l'archer et à l'arc.
"""

def spine_dynamique_requise(
    W_usine,           # Puissance de l'arc à l'allonge de référence (lb)
    L_archer,          # Allonge réelle de l'archer (pouces)
    L_usine=28,        # Allonge de référence usine (pouces)
    base_offset=5,     # Offset de base (correction Rowan)
    tip_weight_g=0,    # Poids de la pointe (en grammes)
    string_type=None,  # 'modern' ou 'dacron'
    silencer_type=None,# 'heavy' ou 'light'
    window_position_mm=0  # Décalage du center-cut (mm)
):
    """
    Retourne :
    - D_dynamic_lb : charge dynamique cible (en livres)
    - spine_stat_ata : spine statique recommandé (ATA, en millièmes de pouce)
    - offsets : détails des corrections appliquées
    """
    # 1) Charge effective basée sur l'allonge
    W_eff = W_usine * (L_archer / L_usine)

    # 2) Correction due à la variation d'allonge
    delta_W = (L_archer - L_usine) * 5

    # 3) Correction poids de pointe
    grains = tip_weight_g * 15.4324
    tip_offset = -5 * (grains / 175) if tip_weight_g > 0 else 0

    # 4) Correction type de corde
    if string_type == 'modern':
        string_offset = 5
    elif string_type == 'dacron':
        string_offset = -5
    else:
        string_offset = 0  # Valeur par défaut si non précisé

    # 5) Correction silencieux
    if silencer_type == 'heavy':
        silencer_offset = -2
    elif silencer_type == 'light':
        silencer_offset = -1
    else:
        silencer_offset = 0

    # 6) Correction center-cut
    center_offset = 5 if window_position_mm > 0 else 0

    # 7) Calcul de la charge dynamique
    D = W_eff + delta_W + base_offset + tip_offset + string_offset + silencer_offset + center_offset

    # 8) Calcul du spine statique recommandé (ATA)
    spine_stat = (26 / D) * 1000 if D > 0 else 0

    return {
        'D_dynamic_lb': round(D, 1),
        'spine_stat_ata': round(spine_stat),
        'offsets': {
            'tip_offset_lb': round(tip_offset, 1),
            'string_offset_lb': string_offset,
            'silencer_offset_lb': silencer_offset,
            'centercut_offset_lb': center_offset,
        }
    }

if __name__ == "__main__":
    # Exemple d'utilisation
    result = spine_dynamique_requise(
        W_usine=50,
        L_archer=29,
        tip_weight_g=11,
        string_type='modern',
        silencer_type='heavy',
        window_position_mm=2
    )
    print(f"Charge dynamique cible : {result['D_dynamic_lb']} lb")
    print(f"Spine statique recommandée : {result['spine_stat_ata']}")
    print("Détails des offsets :", result['offsets'])

