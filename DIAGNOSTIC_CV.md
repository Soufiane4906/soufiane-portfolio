# 🔍 Diagnostic - CV Non Visible

## Problème Rapporté
Le CV en PDF n'est plus visible dans le portfolio.

## Vérifications Effectuées

### ✅ 1. Fichier PDF Existe
```bash
Location: c:\Users\Soufiane\Desktop\resume\soufiane portfolio\Soufiane_Aniba_CV_2025.pdf
Status: ✅ Fichier présent
```

### ✅ 2. Code HTML Présent
```html
<!-- Ligne 447-475 de portfolio.html -->
<section id="cv-academique" class="section cv-section">
    <h2 class="section-title">CV & Parcours Académique</h2>
    
    <div class="cv-preview-container">
        <div class="cv-preview">
            <div class="cv-iframe-container">
                <iframe src="Soufiane_Aniba_CV_2025.pdf" class="cv-iframe" title="CV Soufiane Aniba"></iframe>
                <div class="cv-overlay"></div>
            </div>
        </div>
    </div>
</section>
```

### ✅ 3. Styles CSS Présents
```css
.cv-preview {
    position: relative;
    background: white;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 30px var(--shadow-medium);
    height: 800px; /* ✅ Hauteur définie */
    border: 2px solid var(--primary-red);
}

.cv-iframe {
    width: 100%;
    height: 100%;
    min-height: 1200px; /* ✅ Hauteur minimale */
    border: none;
    display: block;
}

.cv-iframe-container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: auto; /* ✅ Scrollable */
}
```

## Causes Possibles

### 1. 🔒 Blocage du Navigateur
Certains navigateurs bloquent le chargement de PDF dans les iframes pour des raisons de sécurité.

**Solution** :
- Vérifier la console du navigateur (F12)
- Chercher des erreurs de type "Refused to display..." ou "Content Security Policy"

### 2. 📏 Problème de Hauteur CSS
L'iframe ou le conteneur pourrait avoir une hauteur effective de 0.

**Solution** :
Vérifier dans les DevTools (F12 → Inspecteur) si `.cv-preview` a bien 800px de hauteur.

### 3. 🎨 Overlay Masquant le Contenu
L'overlay pourrait masquer le PDF.

**Status** : ❌ Peu probable
- `pointer-events: none` est configuré
- `opacity: 0` par défaut (visible seulement au hover)

### 4. 🌐 Serveur Local
Le PDF nécessite un serveur HTTP pour être affiché dans un iframe.

**Status** : ✅ Serveur actif
- Port 8001 : http://localhost:8001

## 🛠️ Solutions Rapides

### Solution 1 : Vérifier dans le Navigateur
1. Ouvrir http://localhost:8001/portfolio.html
2. Appuyer sur F12 (DevTools)
3. Aller dans l'onglet "Console"
4. Chercher des erreurs rouges
5. Aller dans l'onglet "Réseau" (Network)
6. Recharger la page (Ctrl+R)
7. Vérifier si "Soufiane_Aniba_CV_2025.pdf" est chargé (200 OK)

### Solution 2 : Tester le PDF Direct
Ouvrir directement : http://localhost:8001/Soufiane_Aniba_CV_2025.pdf

Si ça fonctionne → le problème vient de l'iframe
Si ça ne fonctionne pas → le problème vient du serveur ou du fichier

### Solution 3 : Vérifier la Section CV
1. Ouvrir http://localhost:8001/portfolio.html
2. F12 → Inspecteur (Elements)
3. Chercher `<section id="cv-academique">`
4. Vérifier si la section est visible dans le DOM
5. Vérifier les styles calculés de `.cv-preview`

### Solution 4 : Alternative avec Object
Si l'iframe ne fonctionne pas, utiliser `<object>` :

```html
<object data="Soufiane_Aniba_CV_2025.pdf" type="application/pdf" class="cv-iframe">
    <p>Votre navigateur ne supporte pas l'affichage de PDF. 
    <a href="Soufiane_Aniba_CV_2025.pdf">Télécharger le PDF</a></p>
</object>
```

### Solution 5 : Alternative avec Embed
```html
<embed src="Soufiane_Aniba_CV_2025.pdf" type="application/pdf" class="cv-iframe" />
```

## 🧪 Test de Diagnostic

### Étape 1 : Console Browser
```javascript
// Dans la console du navigateur (F12)
document.querySelector('.cv-iframe')
// Doit retourner : <iframe src="Soufiane_Aniba_CV_2025.pdf" ...>

document.querySelector('.cv-preview').style.height
// Doit retourner : "800px"
```

### Étape 2 : Vérifier le Chargement
```javascript
// Dans la console
let iframe = document.querySelector('.cv-iframe');
iframe.onload = function() { console.log('PDF chargé !'); };
iframe.onerror = function() { console.log('Erreur chargement PDF'); };
```

## 📋 Checklist de Diagnostic

- [ ] Le serveur local est actif (http://localhost:8001)
- [ ] Le fichier PDF existe dans le bon dossier
- [ ] Le PDF s'ouvre directement : http://localhost:8001/Soufiane_Aniba_CV_2025.pdf
- [ ] La section `#cv-academique` est présente dans le HTML
- [ ] La section est visible (pas de `display: none`)
- [ ] L'iframe a une hauteur > 0
- [ ] Pas d'erreur dans la console (F12)
- [ ] Le navigateur supporte les PDF dans iframe

## 🔧 Fix Rapide Recommandé

Si le problème persiste, voici une modification CSS pour forcer l'affichage :

```css
.cv-preview {
    min-height: 800px !important;
    display: block !important;
}

.cv-iframe-container {
    min-height: 800px !important;
    display: block !important;
}

.cv-iframe {
    min-height: 800px !important;
    display: block !important;
    visibility: visible !important;
}
```

## 📱 Problème Mobile ?

Si vous testez sur mobile :
- Safari iOS ne supporte pas toujours les PDF dans iframe
- Solution : Utiliser un lien de téléchargement à la place

## 🎯 Prochaines Étapes

1. **Ouvrir le portfolio** : http://localhost:8001/portfolio.html
2. **Scroller jusqu'à la section CV**
3. **Ouvrir DevTools (F12)**
4. **Vérifier la console pour des erreurs**
5. **Rapporter les erreurs trouvées**

## 💡 Information Complémentaire

Le CV est censé apparaître dans la section "CV & Parcours Académique" après :
- La section Certifications
- Avant la section Contact

Navigation directe : http://localhost:8001/portfolio.html#cv-academique

---

**Serveur actif** : http://localhost:8001/portfolio.html
**PDF direct** : http://localhost:8001/Soufiane_Aniba_CV_2025.pdf

Testez ces deux URLs et rapportez ce qui s'affiche !
