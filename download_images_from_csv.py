#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplifié pour télécharger les images depuis le fichier CSV
Version sans Selenium - utilise directement le CSV généré
"""

import os
import csv
import requests
from pathlib import Path
import time

def download_image(url, filepath, name, category):
    """Télécharge une image depuis une URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://www.linkedin.com/',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site'
        }

        response = requests.get(url, headers=headers, timeout=15, stream=True)

        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            file_size = os.path.getsize(filepath)
            print(f"      ✅ Téléchargé - {file_size:,} bytes")
            return True
        else:
            print(f"      ❌ Erreur HTTP {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"      ❌ Erreur réseau: {str(e)[:60]}")
        return False
    except Exception as e:
        print(f"      ❌ Erreur: {str(e)[:60]}")
        return False

def sanitize_filename(name, max_length=50):
    """Nettoie un nom pour en faire un nom de fichier valide"""
    # Enlever les caractères spéciaux
    name = name.replace('Logo de ', '')
    name = name.replace('/', '_')
    name = name.replace('\\', '_')
    name = name.replace(':', '_')
    name = name.replace('*', '_')
    name = name.replace('?', '_')
    name = name.replace('"', '_')
    name = name.replace('<', '_')
    name = name.replace('>', '_')
    name = name.replace('|', '_')
    name = name.replace(' ', '_')

    # Limiter la longueur
    if len(name) > max_length:
        name = name[:max_length]

    return name.strip('_')

def main():
    """Fonction principale"""
    print("═" * 80)
    print("  🚀 TÉLÉCHARGEMENT DES IMAGES DEPUIS LE CSV")
    print("═" * 80)

    # Fichier CSV source
    csv_file = "images_extraites.csv"

    if not Path(csv_file).exists():
        print(f"❌ Fichier {csv_file} non trouvé!")
        print("   Exécutez d'abord: python extract_all_images.py")
        return

    # Créer les dossiers de destination
    output_dir = Path("public/assets/img")
    education_dir = output_dir / "education"
    experience_dir = output_dir / "experience"
    certification_dir = output_dir / "certification"

    for directory in [education_dir, experience_dir, certification_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Dossiers de destination créés:")
    print(f"   • {education_dir}")
    print(f"   • {experience_dir}")
    print(f"   • {certification_dir}")

    # Lire le CSV
    print(f"\n📄 Lecture du fichier CSV: {csv_file}")

    images = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        images = list(reader)

    print(f"   ✓ {len(images)} images trouvées dans le CSV\n")

    # Statistiques
    stats = {
        'total': len(images),
        'success': 0,
        'failed': 0,
        'skipped': 0,
        'by_category': {}
    }

    # Traquer les URLs déjà téléchargées pour éviter les doublons
    downloaded_urls = set()

    print("═" * 80)
    print("  📥 DÉBUT DU TÉLÉCHARGEMENT")
    print("═" * 80)

    # Télécharger chaque image
    for idx, img in enumerate(images, 1):
        category = img['category']
        alt = img['alt']
        url = img['src']

        # Skip si pas d'URL
        if not url or url == '':
            print(f"\n[{idx}/{len(images)}] ⚠️  Image sans URL - ignorée")
            stats['skipped'] += 1
            continue

        # Skip les doublons
        if url in downloaded_urls:
            print(f"\n[{idx}/{len(images)}] ⏭️  Doublon détecté - ignoré")
            print(f"   📝 {alt}")
            stats['skipped'] += 1
            continue

        # Déterminer le dossier de destination
        if category == 'EDUCATION':
            dest_dir = education_dir
            prefix = 'edu'
        elif category == 'EXPERIENCE':
            dest_dir = experience_dir
            prefix = 'exp'
        elif category == 'CERTIFICATION':
            dest_dir = certification_dir
            prefix = 'cert'
        else:
            dest_dir = output_dir
            prefix = 'other'

        # Créer le nom de fichier basé sur le alt text
        clean_name = sanitize_filename(alt)
        if not clean_name:
            clean_name = f"{prefix}_{idx:03d}"

        # Extension (toujours PNG pour les logos LinkedIn)
        ext = '.png'
        filename = f"{clean_name}{ext}"
        filepath = dest_dir / filename

        # Éviter les collisions de noms
        counter = 1
        while filepath.exists():
            filename = f"{clean_name}_{counter}{ext}"
            filepath = dest_dir / filename
            counter += 1

        # Afficher les informations
        print(f"\n[{idx}/{len(images)}] 📦 {category}")
        print(f"   📝 {alt}")
        print(f"   💾 {filename}")
        print(f"   🔗 {url[:80]}...")

        # Télécharger l'image
        success = download_image(url, filepath, alt, category)

        if success:
            stats['success'] += 1
            downloaded_urls.add(url)
        else:
            stats['failed'] += 1

        # Mettre à jour les statistiques par catégorie
        if category not in stats['by_category']:
            stats['by_category'][category] = {'success': 0, 'failed': 0, 'skipped': 0}

        if success:
            stats['by_category'][category]['success'] += 1
        else:
            stats['by_category'][category]['failed'] += 1

        # Petite pause pour ne pas surcharger les serveurs
        time.sleep(0.3)

    # Afficher les statistiques finales
    print("\n" + "═" * 80)
    print("  📊 STATISTIQUES FINALES")
    print("═" * 80)
    print(f"\n✅ Téléchargés avec succès: {stats['success']}")
    print(f"❌ Échecs: {stats['failed']}")
    print(f"⏭️  Ignorés (doublons/vides): {stats['skipped']}")
    print(f"📊 Total traité: {stats['total']}")

    if stats['success'] > 0:
        success_rate = (stats['success'] / (stats['total'] - stats['skipped']) * 100)
        print(f"📈 Taux de réussite: {success_rate:.1f}%")

    print("\n📋 Détails par catégorie:")
    for cat, cat_stats in stats['by_category'].items():
        total = cat_stats['success'] + cat_stats['failed']
        print(f"   • {cat}: {cat_stats['success']}/{total} réussis")

    print("\n" + "═" * 80)
    print("  ✅ TÉLÉCHARGEMENT TERMINÉ!")
    print("═" * 80)
    print(f"\n📁 Images sauvegardées dans:")
    print(f"   • Éducation: {education_dir}")
    print(f"   • Expérience: {experience_dir}")
    print(f"   • Certifications: {certification_dir}")

    # Vérifier combien de fichiers ont été créés
    edu_count = len(list(education_dir.glob('*.png')))
    exp_count = len(list(experience_dir.glob('*.png')))
    cert_count = len(list(certification_dir.glob('*.png')))

    print(f"\n📂 Fichiers créés:")
    print(f"   • Éducation: {edu_count} fichiers")
    print(f"   • Expérience: {exp_count} fichiers")
    print(f"   • Certifications: {cert_count} fichiers")
    print(f"   • Total: {edu_count + exp_count + cert_count} fichiers")

if __name__ == '__main__':
    main()
