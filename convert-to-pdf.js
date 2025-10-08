const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function convertHtmlToPdf() {
    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-default-apps'
        ]
    });

    try {
        const page = await browser.newPage();

        // Optimisation pour une meilleure qualité d'impression
        await page.setViewport({
            width: 1200,
            height: 1600,
            deviceScaleFactor: 2 // Améliore la qualité des images et du texte
        });

        // Chemin vers votre fichier HTML
        const htmlPath = path.join(__dirname, 'cv.html');
        const htmlUrl = `file://${htmlPath}`;

        console.log('🔄 Chargement du CV HTML...');
        await page.goto(htmlUrl, {
            waitUntil: ['networkidle0', 'domcontentloaded'],
            timeout: 30000
        });

        // Attendre que toutes les images soient chargées
        await page.evaluate(() => {
            return Promise.all(
                Array.from(document.images)
                    .filter(img => !img.complete)
                    .map(img => new Promise(resolve => {
                        img.onload = resolve;
                        img.onerror = resolve;
                    }))
            );
        });

        console.log('📄 Génération du PDF en haute qualité...');

        // Configuration PDF optimisée pour la haute qualité
        const pdfBuffer = await page.pdf({
            format: 'A4',
            printBackground: true,
            preferCSSPageSize: true,
            displayHeaderFooter: false,
            margin: {
                top: '0mm',
                right: '0mm',
                bottom: '0mm',
                left: '0mm'
            },
            // Optimisations pour la qualité
            quality: 100,
            omitBackground: false,
            tagged: true,
            outline: false
        });

        // Sauvegarder le PDF
        const outputPath = path.join(__dirname, 'Soufiane_Aniba_CV_2025.pdf');
        fs.writeFileSync(outputPath, pdfBuffer);

        console.log('✅ CV converti avec succès !');
        console.log(`📁 Fichier sauvegardé : ${outputPath}`);
        console.log(`📊 Taille du fichier : ${(pdfBuffer.length / 1024 / 1024).toFixed(2)} MB`);

        return outputPath;

    } catch (error) {
        console.error('❌ Erreur lors de la conversion :', error);
        throw error;
    } finally {
        await browser.close();
    }
}

// Fonction pour vérifier la qualité du PDF généré
async function validatePdf(pdfPath) {
    const stats = fs.statSync(pdfPath);
    const fileSizeInMB = stats.size / (1024 * 1024);

    console.log('\n📋 Informations du PDF généré :');
    console.log(`   📁 Nom : ${path.basename(pdfPath)}`);
    console.log(`   📊 Taille : ${fileSizeInMB.toFixed(2)} MB`);
    console.log(`   📅 Date : ${stats.mtime.toLocaleString('fr-FR')}`);

    if (fileSizeInMB > 0.5) {
        console.log('   ✅ Qualité : Haute qualité (fichier volumineux = bonne résolution)');
    } else {
        console.log('   ⚠️  Qualité : Standard (fichier compact)');
    }
}

// Exécution du script
if (require.main === module) {
    console.log('🚀 Démarrage de la conversion HTML vers PDF...\n');

    convertHtmlToPdf()
        .then(async (outputPath) => {
            await validatePdf(outputPath);
            console.log('\n🎉 Conversion terminée avec succès !');
            console.log('💡 Votre CV PDF haute qualité est prêt à être utilisé.');
        })
        .catch((error) => {
            console.error('\n💥 Échec de la conversion :', error.message);
            process.exit(1);
        });
}

module.exports = { convertHtmlToPdf, validatePdf };
