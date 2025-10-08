#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour télécharger les images en utilisant Selenium
Ouvre le fichier HTML et télécharge toutes les images affichées
"""

import os
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def setup_driver():
    """Configure le driver Chrome avec les options appropriées"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Mode sans interface
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')

    # Activer les logs pour debugging
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--v=1')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Driver Chrome initialisé avec succès")
        return driver
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation du driver: {e}")
        print("\n💡 Assurez-vous que ChromeDriver est installé:")
        print("   pip install selenium")
        print("   pip install webdriver-manager")
        return None

def download_image(url, filepath, category, name):
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

        response = requests.get(url, headers=headers, timeout=10, stream=True)

        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            file_size = os.path.getsize(filepath)
            print(f"   ✅ {name} - {file_size} bytes")
            return True
        else:
            print(f"   ❌ {name} - Erreur HTTP {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ {name} - Erreur: {str(e)[:50]}")
        return False

def extract_images_from_html(driver, html_file):
    """Extrait toutes les images depuis le fichier HTML"""

    # Ouvrir le fichier HTML
    html_path = Path(html_file).absolute()
    file_url = f"file:///{str(html_path).replace(os.sep, '/')}"

    print(f"\n🌐 Ouverture du fichier HTML...")
    print(f"   URL: {file_url}\n")

    driver.get(file_url)

    # Attendre que la page soit chargée
    time.sleep(2)

    print("🔍 Recherche des images dans la page...\n")

    # Trouver toutes les cartes d'images
    image_cards = driver.find_elements(By.CLASS_NAME, "image-card")
    print(f"📦 {len(image_cards)} cartes d'images trouvées\n")

    images_data = []

    for idx, card in enumerate(image_cards, 1):
        try:
            # Extraire les informations de la carte
            img_element = card.find_element(By.TAG_NAME, "img")
            title_element = card.find_element(By.CLASS_NAME, "image-title")
            badge_element = card.find_element(By.CLASS_NAME, "badge")

            img_url = img_element.get_attribute('src')
            img_alt = img_element.get_attribute('alt')
            title = title_element.text
            category = badge_element.text

            images_data.append({
                'index': idx,
                'url': img_url,
                'alt': img_alt,
                'title': title,
                'category': category
            })

        except Exception as e:
            print(f"⚠️  Erreur sur la carte {idx}: {e}")
            continue

    return images_data

def main():
    """Fonction principale"""
    print("═" * 80)
    print("  🚀 TÉLÉCHARGEMENT AUTOMATIQUE DES IMAGES AVEC SELENIUM")
    print("═" * 80)

    # Fichier HTML à analyser
    html_file = "TOUTES_LES_IMAGES.html"

    if not Path(html_file).exists():
        print(f"❌ Fichier {html_file} non trouvé!")
        return

    # Créer les dossiers de destination
    output_dir = Path("public/assets/img")
    education_dir = output_dir / "education"
    experience_dir = output_dir / "experience"
    certification_dir = output_dir / "certification"

    for directory in [education_dir, experience_dir, certification_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Dossiers créés:")
    print(f"   • {education_dir}")
    print(f"   • {experience_dir}")
    print(f"   • {certification_dir}")

    # Initialiser le driver
    driver = setup_driver()

    if not driver:
        print("\n❌ Impossible de continuer sans driver Chrome")
        return

    try:
        # Extraire les images
        images_data = extract_images_from_html(driver, html_file)

        if not images_data:
            print("❌ Aucune image trouvée dans le fichier HTML")
            return

        print(f"\n📊 Total: {len(images_data)} images à télécharger")
        print("═" * 80)

        # Statistiques
        stats = {
            'total': len(images_data),
            'success': 0,
            'failed': 0,
            'by_category': {}
        }

        # Télécharger chaque image
        for img_data in images_data:
            category = img_data['category']
            index = img_data['index']
            title = img_data['title']
            url = img_data['url']

            # Déterminer le dossier de destination
            if category == 'ÉDUCATION':
                dest_dir = education_dir
                prefix = 'edu'
            elif category == 'EXPÉRIENCE':
                dest_dir = experience_dir
                prefix = 'exp'
            elif category == 'CERTIFICATION':
                dest_dir = certification_dir
                prefix = 'cert'
            else:
                dest_dir = output_dir
                prefix = 'other'

            # Créer le nom de fichier
            # Extraire l'extension de l'URL
            if '?' in url:
                base_url = url.split('?')[0]
            else:
                base_url = url

            # Déterminer l'extension
            if 'company-logo' in url or 'profile-treasury' in url:
                ext = '.png'
            else:
                ext = '.png'

            filename = f"{prefix}_{index:03d}{ext}"
            filepath = dest_dir / filename

            # Afficher les informations
            print(f"\n[{index}/{len(images_data)}] {category}")
            print(f"   📝 {title}")
            print(f"   🔗 {url[:80]}...")

            # Télécharger l'image
            success = download_image(url, filepath, category, title)

            if success:
                stats['success'] += 1
            else:
                stats['failed'] += 1

            # Mettre à jour les statistiques par catégorie
            if category not in stats['by_category']:
                stats['by_category'][category] = {'success': 0, 'failed': 0}

            if success:
                stats['by_category'][category]['success'] += 1
            else:
                stats['by_category'][category]['failed'] += 1

            # Petite pause pour ne pas surcharger les serveurs
            time.sleep(0.5)

        # Afficher les statistiques finales
        print("\n" + "═" * 80)
        print("  📊 STATISTIQUES FINALES")
        print("═" * 80)
        print(f"\n✅ Réussis: {stats['success']}/{stats['total']}")
        print(f"❌ Échoués: {stats['failed']}/{stats['total']}")
        print(f"📈 Taux de réussite: {(stats['success']/stats['total']*100):.1f}%")

        print("\n📋 Par catégorie:")
        for cat, cat_stats in stats['by_category'].items():
            total = cat_stats['success'] + cat_stats['failed']
            print(f"   • {cat}: {cat_stats['success']}/{total} réussis")

        print("\n" + "═" * 80)
        print("  ✅ TÉLÉCHARGEMENT TERMINÉ!")
        print("═" * 80)
        print(f"\n📁 Images sauvegardées dans: {output_dir}")

    except Exception as e:
        print(f"\n❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

    finally:
        print("\n🔚 Fermeture du navigateur...")
        driver.quit()
        print("✅ Navigateur fermé")

if __name__ == '__main__':
    main()
