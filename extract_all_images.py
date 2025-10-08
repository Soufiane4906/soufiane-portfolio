#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour extraire toutes les URLs d'images des fichiers HTML
et les rassembler dans un fichier CSV lisible
"""

import re
import csv
from pathlib import Path
from html.parser import HTMLParser

class ImageExtractor(HTMLParser):
    """Parser HTML pour extraire les images"""

    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            image_data = {
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', ''),
                'width': attrs_dict.get('width', ''),
                'height': attrs_dict.get('height', '')
            }
            if image_data['src']:  # Seulement si l'image a un src
                self.images.append(image_data)

def extract_images_from_html(html_file):
    """Extrait les images d'un fichier HTML"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        parser = ImageExtractor()
        parser.feed(content)

        return parser.images
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de {html_file}: {e}")
        return []

def clean_url(url):
    """Nettoie l'URL pour la rendre plus lisible"""
    # Enlever les paramètres de temps d'expiration pour plus de clarté
    return url.split('&amp;')[0] if '&amp;' in url else url

def categorize_image(filename, alt_text):
    """Catégorise l'image selon le fichier source"""
    if 'EDUCTION' in filename:
        return 'EDUCATION'
    elif 'EXPERIENCE' in filename:
        return 'EXPERIENCE'
    elif 'LICENCE' in filename or 'certif' in filename:
        return 'CERTIFICATION'
    return 'AUTRE'

def main():
    """Fonction principale"""
    print("🔍 Extraction des images depuis les fichiers HTML...\n")

    # Fichiers à analyser
    html_files = [
        'EDUCTION.HTML',
        'EXPERIENCE.HTML',
        'LICENCEandcertif.html'
    ]

    all_images = []

    # Extraire les images de chaque fichier
    for html_file in html_files:
        file_path = Path(html_file)
        if file_path.exists():
            print(f"📄 Analyse de {html_file}...")
            images = extract_images_from_html(file_path)

            # Ajouter la catégorie et le fichier source
            for img in images:
                img['category'] = categorize_image(html_file, img['alt'])
                img['source_file'] = html_file
                # Nettoyer l'URL
                img['src_clean'] = clean_url(img['src'])
                all_images.append(img)

            print(f"   ✓ {len(images)} images trouvées")
        else:
            print(f"   ⚠️  Fichier non trouvé: {html_file}")

    print(f"\n📊 Total: {len(all_images)} images extraites\n")

    # Sauvegarder dans un CSV
    csv_file = 'images_extraites.csv'

    if all_images:
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            fieldnames = ['category', 'alt', 'src_clean', 'width', 'height', 'source_file', 'src']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(all_images)

        print(f"✅ Fichier CSV créé: {csv_file}")
        print(f"   Vous pouvez l'ouvrir avec Excel ou un éditeur de texte\n")

        # Afficher un résumé par catégorie
        print("📋 Résumé par catégorie:")
        categories = {}
        for img in all_images:
            cat = img['category']
            categories[cat] = categories.get(cat, 0) + 1

        for cat, count in sorted(categories.items()):
            print(f"   • {cat}: {count} images")

        # Afficher les premières images pour vérification
        print("\n🔗 Aperçu des images extraites:")
        print("-" * 100)
        for i, img in enumerate(all_images[:10], 1):
            print(f"\n{i}. [{img['category']}] {img['alt']}")
            print(f"   URL: {img['src_clean'][:80]}...")
            print(f"   Fichier: {img['source_file']}")

        if len(all_images) > 10:
            print(f"\n... et {len(all_images) - 10} autres images (voir le fichier CSV pour la liste complète)")
    else:
        print("❌ Aucune image trouvée dans les fichiers HTML")

if __name__ == '__main__':
    main()
