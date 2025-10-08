#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script optimisé pour télécharger les images
Combine CSV et téléchargement asynchrone pour plus de rapidité
"""

import os
import csv
import requests
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_image(img_data):
    """Télécharge une image - Version thread-safe"""
    url = img_data['url']
    filepath = img_data['filepath']
    alt = img_data['alt']
    category = img_data['category']
    idx = img_data['idx']
    total = img_data['total']

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'image/*',
            'Referer': 'https://www.linkedin.com/'
        }

        response = requests.get(url, headers=headers, timeout=10, stream=True)

        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            file_size = os.path.getsize(filepath)
            result = {
                'success': True,
                'idx': idx,
                'total': total,
                'category': category,
                'alt': alt,
                'filename': filepath.name,
                'size': file_size
            }
            return result
        else:
            return {
                'success': False,
                'idx': idx,
                'total': total,
                'category': category,
                'alt': alt,
                'error': f'HTTP {response.status_code}'
            }

    except Exception as e:
        return {
            'success': False,
            'idx': idx,
            'total': total,
            'category': category,
            'alt': alt,
            'error': str(e)[:50]
        }

def sanitize_filename(name, max_length=50):
    """Nettoie un nom pour en faire un nom de fichier valide"""
    name = name.replace('Logo de ', '')
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        name = name.replace(char, '_')
    name = name.replace(' ', '_')

    if len(name) > max_length:
        name = name[:max_length]

    return name.strip('_')

def main():
    """Fonction principale"""
    print("═" * 80)
    print("  🚀 TÉLÉCHARGEMENT RAPIDE DES IMAGES (Multi-threading)")
    print("═" * 80)

    csv_file = "images_extraites.csv"

    if not Path(csv_file).exists():
        print(f"❌ Fichier {csv_file} non trouvé!")
        return

    # Créer les dossiers
    output_dir = Path("public/assets/img")
    dirs = {
        'EDUCATION': output_dir / "education",
        'EXPERIENCE': output_dir / "experience",
        'CERTIFICATION': output_dir / "certification"
    }

    for directory in dirs.values():
        directory.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Dossiers prêts")

    # Lire le CSV
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        images = list(reader)

    print(f"📄 {len(images)} images à télécharger\n")

    # Préparer les tâches (sans doublons)
    tasks = []
    seen_urls = set()

    for idx, img in enumerate(images, 1):
        category = img['category']
        alt = img['alt']
        url = img['src']

        if not url or url in seen_urls:
            continue

        seen_urls.add(url)

        dest_dir = dirs.get(category, output_dir)
        clean_name = sanitize_filename(alt)
        if not clean_name:
            clean_name = f"image_{idx:03d}"

        filename = f"{clean_name}.png"
        filepath = dest_dir / filename

        # Éviter les collisions
        counter = 1
        while filepath.exists():
            filename = f"{clean_name}_{counter}.png"
            filepath = dest_dir / filename
            counter += 1

        tasks.append({
            'idx': idx,
            'total': len(images),
            'url': url,
            'filepath': filepath,
            'alt': alt,
            'category': category
        })

    print(f"📦 {len(tasks)} images uniques à télécharger")
    print("═" * 80)

    # Statistiques
    stats = {
        'success': 0,
        'failed': 0,
        'by_category': {}
    }

    # Téléchargement en parallèle
    max_workers = 5  # Nombre de téléchargements simultanés

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_image, task): task for task in tasks}

        for future in as_completed(futures):
            result = future.result()

            idx = result['idx']
            total = result['total']
            category = result['category']
            alt = result['alt']

            if result['success']:
                stats['success'] += 1
                print(f"✅ [{idx}/{total}] {category}")
                print(f"   📝 {alt}")
                print(f"   💾 {result['filename']} ({result['size']:,} bytes)")

                if category not in stats['by_category']:
                    stats['by_category'][category] = {'success': 0, 'failed': 0}
                stats['by_category'][category]['success'] += 1
            else:
                stats['failed'] += 1
                print(f"❌ [{idx}/{total}] {category}")
                print(f"   📝 {alt}")
                print(f"   ⚠️  {result['error']}")

                if category not in stats['by_category']:
                    stats['by_category'][category] = {'success': 0, 'failed': 0}
                stats['by_category'][category]['failed'] += 1

    # Résumé final
    print("\n" + "═" * 80)
    print("  📊 RÉSUMÉ FINAL")
    print("═" * 80)
    print(f"\n✅ Réussis: {stats['success']}")
    print(f"❌ Échoués: {stats['failed']}")
    print(f"📊 Total: {len(tasks)}")

    if stats['success'] > 0:
        print(f"📈 Taux de réussite: {(stats['success']/len(tasks)*100):.1f}%")

    print("\n📋 Par catégorie:")
    for cat, cat_stats in stats['by_category'].items():
        total = cat_stats['success'] + cat_stats['failed']
        print(f"   • {cat}: {cat_stats['success']}/{total} réussis")

    # Vérification finale
    print("\n📂 Fichiers créés:")
    for cat, directory in dirs.items():
        count = len(list(directory.glob('*.png')))
        print(f"   • {cat}: {count} fichiers dans {directory.name}/")

    print("\n" + "═" * 80)
    print("  ✅ TERMINÉ!")
    print("═" * 80)

if __name__ == '__main__':
    main()
