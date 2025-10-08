#!/usr/bin/env python3
"""
Script d'extraction d'images depuis les pages LinkedIn
Télécharge toutes les images et génère metadata.json
"""

import requests
import json
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import re
from datetime import datetime

# Configuration
BASE_DIR = Path("public/assets/img")
METADATA_FILE = Path("public/assets/metadata.json")

# Données des images à télécharger
IMAGES_DATA = {
    "education": [
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQGFGluKlFLKbg/company-logo_100_100/B4EZVIMm_gG0AA-/0/1740673020369/univ_cotedazur_logo",
            "alt": "Logo de Université Côte d'Azur",
            "institution": "Université Côte d'Azur",
            "category": "education",
            "type": "university"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQE_Fu9hueUY4g/company-logo_100_100/B4EZZsp0_oHEAU-/0/1745579626980/ecole_marocaine_des_sciences_de_lingnieur_logo",
            "alt": "Logo de Ecole Marocaine des Sciences de l'ingénieur",
            "institution": "EMSI",
            "category": "education",
            "type": "engineering_school"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C4E0BAQHsmvJCblF1VA/company-logo_100_100/company-logo_100_100/0/1652945941816/fstm_logo",
            "alt": "Logo de Faculté des Sciences et Techniques Mohammedia",
            "institution": "FST Mohammedia",
            "category": "education",
            "type": "university"
        }
    ],
    "experience": [
        {
            "url": "https://media.licdn.com/dms/image/v2/D4D0BAQH-ZV832H4sdA/company-logo_100_100/company-logo_100_100/0/1705572256355/capgemini_logo",
            "alt": "Logo de Capgemini",
            "company": "Capgemini",
            "category": "experience",
            "type": "company",
            "industry": "IT Consulting"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQHCmuWqR_iuJA/company-logo_100_100/company-logo_100_100/0/1703856942365/ola_energy_group_logo",
            "alt": "Logo de OLA Energy",
            "company": "OLA Energy",
            "category": "experience",
            "type": "company",
            "industry": "Energy"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQF2qiBAi7Z96g/company-logo_100_100/company-logo_100_100/0/1681224346053/siliadsarl_logo",
            "alt": "Logo de SILIAD",
            "company": "SILIAD",
            "category": "experience",
            "type": "company",
            "industry": "Software Development"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C560BAQFcoH7OrmEgyA/company-logo_100_100/company-logo_100_100/0/1631326836331",
            "alt": "Logo de ONP Office National des Pêches",
            "company": "ONP",
            "category": "experience",
            "type": "company",
            "industry": "Fisheries"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQGRyLYTNz-RJg/company-logo_100_100/company-logo_100_100/0/1695032888376/alami_ecom_logo",
            "alt": "Logo de Alami ecom",
            "company": "Alami ecom",
            "category": "experience",
            "type": "company",
            "industry": "E-commerce"
        }
    ],
    "certifications": [
        {
            "url": "https://media.licdn.com/dms/image/v2/D560BAQGiz5ecgpCtkA/company-logo_100_100/company-logo_100_100/0/1688684715866/ibm_logo",
            "alt": "Logo de IBM",
            "provider": "IBM",
            "category": "certification",
            "type": "tech_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C4D0BAQHTIj3QmQ5N0A/company-logo_100_100/company-logo_100_100/0/1656443889325",
            "alt": "Logo de Google Cloud Training Online",
            "provider": "Google Cloud",
            "category": "certification",
            "type": "cloud_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQH1qwoIk9cWIQ/company-logo_100_100/company-logo_100_100/0/1724256453909/certiprof_logo",
            "alt": "Logo de Certiprof",
            "provider": "Certiprof",
            "category": "certification",
            "type": "scrum_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D560BAQHBmbxCDP0JQQ/company-logo_100_100/B56ZlkdQSaI8AQ-/0/1758327015620/meta_logo",
            "alt": "Logo de Meta",
            "provider": "Meta",
            "category": "certification",
            "type": "tech_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4D0BAQGRYxJEhCli5Q/company-logo_100_100/company-logo_100_100/0/1694968580203/biginterview_logo",
            "alt": "Logo de Big Interview",
            "provider": "Big Interview",
            "category": "certification",
            "type": "career_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C560BAQG3lm3m1nOaHA/company-logo_100_100/company-logo_100_100/0/1674016387263/whizlabs_software_logo",
            "alt": "Logo de Whizlabs",
            "provider": "Whizlabs",
            "category": "certification",
            "type": "cloud_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/D4E0BAQGv3cqOuUMY7g/company-logo_100_100/B4EZmhegXHGcAU-/0/1759350753990/google_logo",
            "alt": "Logo de Google",
            "provider": "Google",
            "category": "certification",
            "type": "tech_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C4E0BAQHnbnsnJlBiZg/company-logo_100_100/company-logo_100_100/0/1630601168515/university_of_pennsylvania_logo",
            "alt": "Logo de University of Pennsylvania",
            "provider": "University of Pennsylvania",
            "category": "certification",
            "type": "university_certification"
        },
        {
            "url": "https://media.licdn.com/dms/image/v2/C4E0BAQFGfERBPGurCg/company-logo_100_100/company-logo_100_100/0/1631307390795",
            "alt": "Logo de University of Michigan",
            "provider": "University of Michigan",
            "category": "certification",
            "type": "university_certification"
        }
    ]
}

def clean_filename(text):
    """Nettoie le texte pour créer un nom de fichier valide"""
    # Remplacer les caractères spéciaux
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '_', text)
    return text.strip('_')

def download_image(url, category, name, index):
    """Télécharge une image depuis une URL"""
    try:
        # Ajouter des paramètres pour éviter l'expiration
        if '?' not in url:
            url = url + '?e=1762992000&v=beta'

        print(f"📥 Téléchargement: {name}...")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Déterminer l'extension
        content_type = response.headers.get('content-type', '')
        if 'png' in content_type:
            ext = 'png'
        elif 'jpeg' in content_type or 'jpg' in content_type:
            ext = 'jpg'
        else:
            ext = 'png'  # Par défaut

        # Créer le nom de fichier
        clean_name = clean_filename(name)
        filename = f"{category}_{index:03d}_{clean_name}.{ext}"

        # Créer le chemin complet
        category_dir = BASE_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)

        filepath = category_dir / filename

        # Sauvegarder l'image
        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"  ✅ Sauvegardé: {filepath}")

        return {
            "filename": filename,
            "path": str(filepath.relative_to(Path("public"))),
            "size": len(response.content),
            "format": ext
        }

    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return None

def generate_metadata():
    """Génère le fichier metadata.json avec toutes les informations"""

    print("\n🎨 EXTRACTEUR D'IMAGES LINKEDIN")
    print("=" * 50)

    # Créer la structure de dossiers
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    metadata = {
        "generated_at": datetime.now().isoformat(),
        "total_images": 0,
        "categories": {},
        "images": []
    }

    total_downloaded = 0

    # Traiter chaque catégorie
    for category, images_list in IMAGES_DATA.items():
        print(f"\n📁 Catégorie: {category.upper()}")
        print("-" * 40)

        category_count = 0

        for idx, image_data in enumerate(images_list, 1):
            url = image_data['url']
            name = image_data.get('institution') or image_data.get('company') or image_data.get('provider', f'{category}_{idx}')

            # Télécharger l'image
            download_result = download_image(url, category, name, idx)

            if download_result:
                # Créer l'entrée de métadonnées
                metadata_entry = {
                    "id": f"{category}_{idx:03d}",
                    "category": category,
                    **image_data,
                    **download_result,
                    "downloaded_at": datetime.now().isoformat()
                }

                metadata["images"].append(metadata_entry)
                category_count += 1
                total_downloaded += 1

        metadata["categories"][category] = {
            "count": category_count,
            "description": f"Images pour {category}"
        }

        print(f"✅ {category_count} images téléchargées pour {category}")

    metadata["total_images"] = total_downloaded

    # Sauvegarder les métadonnées
    METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"\n📊 RÉSUMÉ")
    print("=" * 50)
    print(f"✅ Total d'images téléchargées: {total_downloaded}")
    print(f"📁 Dossier de destination: {BASE_DIR}")
    print(f"📄 Métadonnées: {METADATA_FILE}")

    # Afficher les statistiques par catégorie
    print(f"\n📈 STATISTIQUES PAR CATÉGORIE:")
    for category, stats in metadata["categories"].items():
        print(f"  • {category}: {stats['count']} images")

    return metadata

def main():
    """Fonction principale"""
    try:
        metadata = generate_metadata()

        print(f"\n🎉 EXTRACTION TERMINÉE AVEC SUCCÈS!")
        print(f"📦 {metadata['total_images']} images prêtes à être utilisées")

    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
