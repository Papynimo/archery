"""
spine_calculator.py

Module Python to calculate the required dynamic spine and recommended static ATA spine 
for wooden arrows based on bow draw weight, archer's draw length, tip weight, string type,
silencer type, and window (center-cut) position.
"""

def spine_dynamique_requise(
    W_usine,           # Draw weight at L_usine (lb)
    L_archer,          # Archer's draw length (inch)
    L_usine=28,        # Factory reference draw length (inch)
    base_offset=5,     # Rowan base correction (lb)
    tip_weight_g=0,    # Tip weight (grams)
    string_type=None,  # 'modern' or 'dacron'
    silencer_type=None,# 'heavy' or 'light'
    window_position_mm=0  # Center-cut offset (mm)
):
    """
    Retourne la charge dynamique cible (lb) et la spine statique ATA (millièmes de pouce).
    """
    # 1) Charge effective selon l'allonge
    W_eff = W_usine * (L_archer / L_usine)
    # 2) Ajustement selon la longueur de flèche
    delta_W = (L_archer - L_usine) * 5
    # 3) Correction poids de pointe (g -> grains -> lb)
    grains = tip_weight_g * 15.4324
    tip_offset = -5 * (grains / 175) if tip_weight_g > 0 else 0
    # 4) Correction type de corde
    if string_type == 'modern':
        string_offset = 5
    elif string_type == 'dacron':
        string_offset = -5
    else:
        string_offset = 0
    # 5) Correction silencieux
    if silencer_type == 'heavy':
        silencer_offset = -2
    elif silencer_type == 'light':
        silencer_offset = -1
    else:
        silencer_offset = 0
    # 6) Correction center-cut
    center_offset = 5 if window_position_mm > 0 else 0
    # 7) Charge dynamique cible
    D = W_eff + delta_W + base_offset + tip_offset + string_offset + silencer_offset + center_offset
    # 8) Spine statique ATA (millièmes de pouce)
    spine_stat = (26 / D) * 1000
    return {
        'D_dynamic_lb': D,
        'spine_stat_ata': spine_stat,
        'offsets': {
            'tip_offset_lb': tip_offset,
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
    print(f"Charge dynamique cible : {result['D_dynamic_lb']:.1f} lb")
    print(f"Spine statique recommandée : {result['spine_stat_ata']:.0f}")
    print("Détails des offsets :", result['offsets'])
