# Guide de Mise en Place des Logos des Projets

## 📁 Structure des Dossiers

Les logos des projets doivent être placés dans :
```
soufiane portfolio/
└── public/
    └── assets/
        └── img/
            └── projects/
                ├── automotive.png
                ├── blablatrip.png
                ├── alophone.png
                └── moroccautoparts.png
```

---

## 🖼️ Logos à Placer

### 1. **Automotive.ma**
- **Fichier source**: `Automotive.ma.png` (fourni en pièce jointe)
- **Destination**: `public/assets/img/projects/automotive.png`
- **Dimensions recommandées**: 200x200px minimum
- **Format**: PNG avec fond transparent de préférence

### 2. **BlaBlaTrip (BBTies)**
- **Fichier source**: `BBTies.png` (fourni en pièce jointe)
- **Destination**: `public/assets/img/projects/blablatrip.png`
- **Note**: BBTies est le nom technique de BlaBlaTrip
- **Dimensions recommandées**: 200x200px minimum
- **Format**: PNG avec fond transparent de préférence

### 3. **Allo Phone**
- **Fichier source**: `Alo Phone.png` (fourni en pièce jointe)
- **Destination**: `public/assets/img/projects/alophone.png`
- **Dimensions recommandées**: 200x200px minimum
- **Format**: PNG avec fond transparent de préférence

### 4. **Morocco AutoPièces**
- **Fichier source**: `Morocco AutoPièces.png` (fourni en pièce jointe)
- **Destination**: `public/assets/img/projects/moroccautoparts.png`
- **Dimensions recommandées**: 200x200px minimum
- **Format**: PNG avec fond transparent de préférence

---

## ✨ Améliorations du Style Apportées

### 1. **PDF Preview - Défilement Sans Navigation**
✅ **Problème résolu** : Le PDF peut maintenant défiler sans changer d'onglet
- Hauteur augmentée à 800px
- `overflow: auto` sur le conteneur
- Bordure colorée (rouge Palestine en mode clair, vert Maroc en mode sombre)

### 2. **Logos des Projets**
✅ **Nouveau style** `.project-logo` ajouté :
- Taille : 70x70px
- Bordure arrondie : 16px
- Effet de survol : rotation de 5° et zoom 1.1x
- Dégradé Palestine-Maroc en arrière-plan
- Bordure dynamique qui devient rouge au survol
- Ombre portée élégante

### 3. **Icônes des Projets**
✅ **Couleurs mises à jour** avec la palette Palestine-Maroc :
- **Automotive** : Dégradé rouge (#C1272D → #ff6b6b)
- **Travel/BlaBlaTrip** : Dégradé vert (#006233 → #44a08d)
- **E-commerce** : Dégradé or (#D4AF37 → #feca57)
- Effet de survol : rotation de -5° et zoom 1.1x

### 4. **Cartes de Projets**
✅ **Améliorations** :
- Bordure supérieure en dégradé Palestine-Maroc
- Effet hover : élévation de 10px avec zoom 1.02x
- Bordure devient verte au survol
- Ombres plus prononcées et colorées

---

## 🎨 Palette de Couleurs Palestine-Maroc

### Couleurs Principales
- **Rouge Palestine** : `#C1272D`
- **Vert Maroc** : `#006233`
- **Blanc** : `#FFFFFF`
- **Bleu Accent** : `#6050DC`
- **Or Accent** : `#D4AF37`
- **Turquoise** : `#128C7E`
- **Sable Neutre** : `#E0C097`

### Dégradés
- **Primaire** : Rouge → Vert
- **Secondaire** : Vert → Rouge
- **Accent** : Bleu → Or

---

## 📝 Commandes pour Copier les Logos

### Sous Windows (PowerShell)
```powershell
# Créer le dossier projects s'il n'existe pas
mkdir "public\assets\img\projects" -Force

# Copier les logos (depuis le dossier racine)
Copy-Item "Automotive.ma.png" "public\assets\img\projects\automotive.png"
Copy-Item "BBTies.png" "public\assets\img\projects\blablatrip.png"
Copy-Item "Alo Phone.png" "public\assets\img\projects\alophone.png"
Copy-Item "Morocco AutoPièces.png" "public\assets\img\projects\moroccautoparts.png"
```

### Sous Linux/Mac (Bash)
```bash
# Créer le dossier projects
mkdir -p public/assets/img/projects/

# Copier les logos
cp "Automotive.ma.png" "public/assets/img/projects/automotive.png"
cp "BBTies.png" "public/assets/img/projects/blablatrip.png"
cp "Alo Phone.png" "public/assets/img/projects/alophone.png"
cp "Morocco AutoPièces.png" "public/assets/img/projects/moroccautoparts.png"
```

---

## ✅ Checklist de Vérification

Avant de tester le portfolio, assurez-vous que :

- [ ] Le dossier `public/assets/img/projects/` existe
- [ ] Les 4 logos sont copiés avec les bons noms de fichiers
- [ ] Les fichiers sont en format PNG
- [ ] Les dimensions sont au minimum 200x200px
- [ ] Le portfolio.html a été sauvegardé
- [ ] Le portfolio-style.css a été sauvegardé

---

## 🚀 Test du Portfolio

### 1. Ouvrir le portfolio
```bash
# Méthode 1 : Serveur Python
cd "soufiane portfolio"
python -m http.server 8000

# Puis ouvrir : http://localhost:8000/portfolio.html
```

### 2. Vérifications Visuelles
- ✅ Les logos des 4 projets s'affichent correctement
- ✅ L'effet hover fonctionne (rotation + zoom)
- ✅ Le PDF défile sans changer d'onglet
- ✅ Les couleurs Palestine-Maroc sont visibles
- ✅ Les 20 certifications sont affichées dans le slider
- ✅ La navigation entre certifications fonctionne

---

## 📊 Résumé des Modifications

### Fichiers Modifiés
1. `portfolio.html`
   - Chemins des logos mis à jour
   - Section BlaBlaTrip enrichie (description combinant BBTies)
   - Suppression de la duplication BlaBlaTrip

2. `portfolio-style.css`
   - Nouveau style `.project-logo` avec effets hover
   - Style `.cv-preview` amélioré pour défilement
   - Couleurs des `.project-icon` mises à jour
   - Hauteur du PDF preview augmentée à 800px

### Nouveaux Fichiers
- `public/assets/img/projects/.gitkeep` (dossier créé)

---

## 🎯 Résultat Final

**Portfolio avec** :
- ✅ 4 projets avec logos professionnels
- ✅ 20 certifications complètes avec IDs
- ✅ Preview PDF scrollable
- ✅ Design Palestine-Maroc cohérent
- ✅ Animations et effets modernes
- ✅ Mode clair/sombre fonctionnel

**Performance** :
- ✅ Tous les assets en local
- ✅ Chargement rapide
- ✅ Pas de dépendances externes pour les images
