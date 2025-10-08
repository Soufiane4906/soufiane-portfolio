# 🔧 Solution - CV Non Visible

## 🎯 Problème
Le CV en PDF n'apparaît pas dans le portfolio.

## ✅ Vérifications Faites

1. **Fichier PDF** : ✅ Existe (`Soufiane_Aniba_CV_2025.pdf`)
2. **Code HTML** : ✅ Présent et correct
3. **Styles CSS** : ✅ Configurés (hauteur 800px)
4. **Serveur local** : ✅ Actif sur port 8001

## 🧪 Page de Test Créée

**Fichier** : `test-cv.html`
**URL** : http://localhost:8001/test-cv.html

Cette page teste 3 méthodes d'affichage du PDF :
1. `<iframe>` (méthode actuelle)
2. `<object>` (alternative recommandée)
3. `<embed>` (ancienne méthode)

## 🔍 Diagnostic

### Causes Possibles

1. **Blocage du Navigateur**
   - Certains navigateurs (Firefox, Chrome) bloquent les PDF dans iframe
   - Solution : Autoriser les PDF dans les paramètres du navigateur

2. **Problème de Chemin**
   - Le PDF doit être dans le même dossier que `portfolio.html`
   - ✅ C'est le cas : `Soufiane_Aniba_CV_2025.pdf`

3. **CORS / Sécurité**
   - Nécessite un serveur HTTP (pas en `file://`)
   - ✅ Serveur actif sur http://localhost:8001

4. **Hauteur CSS**
   - Le conteneur pourrait avoir une hauteur de 0
   - ✅ Configuré à 800px

## 🛠️ Solutions

### Solution 1 : Utiliser la Page de Test ✨

1. Ouvrir : http://localhost:8001/test-cv.html
2. Vérifier quelle méthode fonctionne :
   - Si **iframe** fonctionne → le portfolio devrait fonctionner
   - Si **object** fonctionne → modifier le portfolio
   - Si **aucune** ne fonctionne → problème de navigateur

### Solution 2 : Modifier le Portfolio avec `<object>`

Si l'iframe ne fonctionne pas, remplacer dans `portfolio.html` :

**Avant** (ligne 468) :
```html
<iframe src="Soufiane_Aniba_CV_2025.pdf" class="cv-iframe" title="CV Soufiane Aniba"></iframe>
```

**Après** :
```html
<object data="Soufiane_Aniba_CV_2025.pdf" type="application/pdf" class="cv-iframe">
    <p style="padding: 2rem; text-align: center; color: var(--text-primary);">
        ⚠️ Votre navigateur ne peut pas afficher le PDF.<br>
        <a href="Soufiane_Aniba_CV_2025.pdf" target="_blank" style="color: var(--primary-red); font-weight: bold;">
            Cliquez ici pour ouvrir le PDF
        </a>
    </p>
</object>
```

### Solution 3 : Alternative - Visionneuse d'Image du PDF

Si les PDF ne fonctionnent pas du tout, convertir le PDF en images :

```bash
# Installer ImageMagick puis :
magick convert -density 300 Soufiane_Aniba_CV_2025.pdf -quality 90 cv-page-%d.jpg
```

Puis afficher les images dans un slider.

### Solution 4 : Utiliser PDF.js

Intégrer la bibliothèque PDF.js de Mozilla :

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<canvas id="pdf-canvas"></canvas>
<script>
// Code pour afficher le PDF avec PDF.js
</script>
```

## 📋 Étapes de Dépannage

### Étape 1 : Tester le PDF Directement
```
http://localhost:8001/Soufiane_Aniba_CV_2025.pdf
```

**Si ça fonctionne** → Le fichier est accessible, problème d'affichage
**Si ça ne fonctionne pas** → Problème de fichier ou serveur

### Étape 2 : Vérifier la Console
1. Ouvrir http://localhost:8001/portfolio.html
2. Appuyer sur F12
3. Aller dans "Console"
4. Chercher des erreurs rouges
5. Chercher "Refused to display" ou "CSP"

### Étape 3 : Vérifier les DevTools
1. F12 → Inspecteur (Elements)
2. Chercher `<iframe class="cv-iframe">`
3. Vérifier les styles calculés
4. Vérifier `height`, `width`, `display`

### Étape 4 : Tester sur un Autre Navigateur
- Chrome
- Firefox
- Edge
- Safari (si macOS)

## 🎨 Fix CSS d'Urgence

Si le problème persiste, ajouter dans `portfolio-style.css` :

```css
/* Fix d'urgence pour le CV */
.cv-section {
    display: block !important;
    visibility: visible !important;
}

.cv-preview {
    display: block !important;
    visibility: visible !important;
    min-height: 800px !important;
}

.cv-iframe-container {
    display: block !important;
    visibility: visible !important;
    min-height: 800px !important;
}

.cv-iframe {
    display: block !important;
    visibility: visible !important;
    min-height: 800px !important;
}
```

## 📱 Note pour Mobile

**Important** : Safari sur iOS ne supporte pas les PDF dans iframe !

**Solution mobile** :
```html
<div class="mobile-pdf-notice" style="display: none;">
    <p>Sur mobile, veuillez télécharger le PDF :</p>
    <a href="Soufiane_Aniba_CV_2025.pdf" download class="cv-action-btn">
        📥 Télécharger mon CV
    </a>
</div>

<script>
// Détecter mobile
if (/Android|iPhone|iPad/i.test(navigator.userAgent)) {
    document.querySelector('.cv-preview').style.display = 'none';
    document.querySelector('.mobile-pdf-notice').style.display = 'block';
}
</script>
```

## 🔗 Liens Utiles

- **Portfolio** : http://localhost:8001/portfolio.html
- **Test CV** : http://localhost:8001/test-cv.html
- **PDF Direct** : http://localhost:8001/Soufiane_Aniba_CV_2025.pdf
- **Section CV** : http://localhost:8001/portfolio.html#cv-academique

## ✨ Prochaines Actions

1. **Ouvrir la page de test** : http://localhost:8001/test-cv.html
2. **Vérifier quelle méthode fonctionne** (iframe, object, embed)
3. **Rapporter le résultat** pour adapter la solution
4. **Vérifier la console** (F12) pour des erreurs
5. **Essayer sur un autre navigateur** si nécessaire

## 💡 Astuce Rapide

Si vous êtes pressé, la solution la plus simple :

**Remplacer l'iframe par un bouton qui ouvre le PDF** :

```html
<div class="cv-preview" style="display: flex; align-items: center; justify-content: center; background: var(--gradient-soft);">
    <div style="text-align: center; padding: 3rem;">
        <h3 style="margin-bottom: 2rem; color: var(--text-primary);">📄 Mon CV Professionnel</h3>
        <a href="Soufiane_Aniba_CV_2025.pdf" target="_blank" class="cv-action-btn" style="font-size: 1.2rem; padding: 1.5rem 3rem;">
            <i data-lucide="external-link"></i>
            Ouvrir mon CV
        </a>
    </div>
</div>
```

---

**Fichiers créés pour le diagnostic** :
- `DIAGNOSTIC_CV.md` - Analyse détaillée du problème
- `test-cv.html` - Page de test avec 3 méthodes d'affichage
- `SOLUTION_CV.md` - Ce fichier avec toutes les solutions

**Testez maintenant** : http://localhost:8001/test-cv.html
