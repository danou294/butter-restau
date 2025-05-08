
import pandas as pd
import json

# Charger le fichier Excel
file_path = "Echantillon.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse('Feuil1')

# Nettoyer les en-têtes
df_cleaned = df.iloc[1:].copy()
df_cleaned.columns = df.iloc[0]
df_cleaned.columns.name = None

# Définir les groupes de tags
tags_columns = {
    "restaurant_type": [
        'Restaurant', 'Restaurant haut de gamme', 'Restaurant gastronomique', 'Restaurant étoilé',
        'Brasserie', 'Cave à manger', '"Fast" (à emporter, sandwicherie...)',
        'Boulangerie/pâtisserie', 'Concept brunch', 'Concept goûter',
        'Coffee shop/salon de thé', 'Bar'
    ],
    "moment": ['Petit-déjeuner', 'Brunch', 'Déjeuner', 'Goûter', 'Apéro', 'Dîner'],
    "location_type": ['Dans la rue', 'Dans une galerie', 'Dans un musée', 'Dans un monument', 'Dans un hôtel'],
    "ambiance": ['Classique', 'Convivial', 'Intimiste/tamisé', 'Familial', 'Festif'],
    "price_range": ['€', '€€', '€€€', '€€€€'],
    "cuisine": [
        'Africain', 'Américain', 'Chinois', 'Coréen', 'Colombien', 'Français', 'Grec',
        'Indien', 'Israélien', 'Italien', 'Japonais', 'Libanais', 'Mexicain', 'Oriental',
        'Péruvien', 'Sud-Américain', 'Thaï', 'Vietnamien'
    ],
    "diet": [
        'Casher (certifié)', 'Casher friendly (tout est casher mais pas de teouda)',
        'Viande casher', 'Offre de vins casher', 'Hallal (certifié)', 'Viande hallal',
        'Végétarien', 'Vegan'
    ],
    "extras": ["Avez-vous d'autres précisions à nous apporter sur votre établissement ?"]
}

# Fonction pour extraire les tags d’un groupe
def collect_tags(row, columns):
    return [col for col in columns if col in row and pd.notna(row[col]) and str(row[col]).strip().lower() not in ["non", "nan", ""]]

# Structuration des données
structured_data = []

for _, row in df_cleaned.iterrows():
    entry = {
        "name": row.get("Nom de l'établissement"),
        "true_name": row.get("Vrai nom"),
        "address": row.get("Adresse(s)"),
        "phone": row.get("Numéro de téléphone"),
        "email": row.get("Mail"),
        "website": row.get("Site web"),
        "google_maps": row.get("Lien google maps"),
        "reservation": row.get("Lien de réservation"),
        "instagram": row.get("Lien de votre compte instagram"),
        "plus": row.get("Les +"),
        "tag_initial": str(row["Tag"]) if pd.notna(row["Tag"]) else "",
        "restaurant_type": ", ".join(collect_tags(row, tags_columns["restaurant_type"])),
        "moment": ", ".join(collect_tags(row, tags_columns["moment"])),
        "location_type": ", ".join(collect_tags(row, tags_columns["location_type"])),
        "ambiance": ", ".join(collect_tags(row, tags_columns["ambiance"])),
        "price_range": ", ".join(collect_tags(row, tags_columns["price_range"])),
        "cuisine": ", ".join(collect_tags(row, tags_columns["cuisine"])),
        "diet": ", ".join(collect_tags(row, tags_columns["diet"])),
        "extras": row.get("Avez-vous d'autres précisions à nous apporter sur votre établissement ?") if pd.notna(row.get("Avez-vous d'autres précisions à nous apporter sur votre établissement ?")) else ""
    }
    structured_data.append(entry)

# Convertir en DataFrame et exporter en CSV
df_result = pd.DataFrame(structured_data)
df_result.to_csv("restaurants_structured_output.csv", index=False, encoding='utf-8')
print("Export terminé : restaurants_structured_output.csv")
