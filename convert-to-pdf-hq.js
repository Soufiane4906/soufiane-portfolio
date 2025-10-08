const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

async function convertHtmlToPdfHighQuality() {
    console.log('🎯 Lancement de la conversion HAUTE QUALITÉ...\n');

    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--no-first-run',
            '--font-render-hinting=none',
            '--disable-font-subpixel-positioning',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection'
        ]
    });

    try {
        const page = await browser.newPage();

        // Configuration viewport pour la meilleure qualité
        await page.setViewport({
            width: 1600,  // Résolution élevée
            height: 2400,
            deviceScaleFactor: 3 // Triple de la résolution normale
        });

        // Optimisation des médias
        await page.emulateMediaType('print');

        const htmlPath = path.join(__dirname, 'cv.html');
        const htmlUrl = `file://${htmlPath}`;

        console.log('📖 Chargement du CV avec optimisations...');
        await page.goto(htmlUrl, {
            waitUntil: ['networkidle0', 'domcontentloaded', 'load'],
            timeout: 60000
        });

        // Injection de styles pour optimiser l'impression
        await page.addStyleTag({
            content: `
                @media print {
                    * {
                        -webkit-print-color-adjust: exact !important;
                        color-adjust: exact !important;
                        print-color-adjust: exact !important;
                    }

                    body {
                        zoom: 1;
                        transform: scale(1);
                    }

                    .container {
                        page-break-inside: avoid;
                        break-inside: avoid;
                    }

                    img {
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges;
                        image-rendering: pixelated;
                    }
                }
            `
        });

        // Attendre le chargement complet des ressources
        await page.evaluate(() => {
            return new Promise((resolve) => {
                // Attendre les images
                const images = Array.from(document.images);
                const imagePromises = images.map(img => {
                    if (img.complete) return Promise.resolve();
                    return new Promise(resolve => {
                        img.onload = resolve;
                        img.onerror = resolve;
                    });
                });

                // Attendre les fonts
                if (document.fonts) {
                    document.fonts.ready.then(() => {
                        Promise.all(imagePromises).then(resolve);
                    });
                } else {
                    Promise.all(imagePromises).then(resolve);
                }
            });
        });

        // Pause supplémentaire pour s'assurer du rendu complet
        await page.waitForTimeout(2000);

        console.log('🎨 Génération du PDF HAUTE QUALITÉ...');

        // Configuration PDF ultra-optimisée
        const pdfOptions = {
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
            // Qualité maximale
            quality: 100,
            omitBackground: false,
            tagged: true,
            outline: false,
            // Options avancées pour la qualité
            timeout: 120000,
            scale: 1.0
        };

        const pdfBuffer = await page.pdf(pdfOptions);

        // Noms de fichiers multiples pour différentes versions
        const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
        const outputPath = path.join(__dirname, `Soufiane_Aniba_CV_HQ_${timestamp}.pdf`);
        const simpleOutputPath = path.join(__dirname, 'Soufiane_Aniba_CV_HighQuality.pdf');

        // Sauvegarder les deux versions
        fs.writeFileSync(outputPath, pdfBuffer);
        fs.writeFileSync(simpleOutputPath, pdfBuffer);

        console.log('✅ CV HAUTE QUALITÉ généré avec succès !');
        console.log(`📁 Fichier principal : ${simpleOutputPath}`);
        console.log(`📁 Fichier horodaté : ${outputPath}`);
        console.log(`📊 Taille : ${(pdfBuffer.length / 1024 / 1024).toFixed(2)} MB`);

        return { outputPath, simpleOutputPath, buffer: pdfBuffer };

    } catch (error) {
        console.error('❌ Erreur lors de la conversion haute qualité :', error);
        throw error;
    } finally {
        await browser.close();
    }
}

// Fonction de comparaison de qualité
async function generateQualityComparison() {
    console.log('🔄 Génération de versions multiples pour comparaison...\n');

    // Version standard
    console.log('1️⃣ Génération version STANDARD...');
    const { convertHtmlToPdf } = require('./convert-to-pdf.js');
    await convertHtmlToPdf();

    // Version haute qualité
    console.log('\n2️⃣ Génération version HAUTE QUALITÉ...');
    await convertHtmlToPdfHighQuality();

    console.log('\n📊 Comparaison des fichiers générés :');

    const standardPath = path.join(__dirname, 'Soufiane_Aniba_CV_2025.pdf');
    const hqPath = path.join(__dirname, 'Soufiane_Aniba_CV_HighQuality.pdf');

    if (fs.existsSync(standardPath)) {
        const standardStats = fs.statSync(standardPath);
        console.log(`   📄 Version Standard : ${(standardStats.size / 1024 / 1024).toFixed(2)} MB`);
    }

    if (fs.existsSync(hqPath)) {
        const hqStats = fs.statSync(hqPath);
        console.log(`   🎯 Version Haute Qualité : ${(hqStats.size / 1024 / 1024).toFixed(2)} MB`);
    }
}

// Exécution
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.includes('--compare')) {
        generateQualityComparison()
            .then(() => {
                console.log('\n🎉 Toutes les versions ont été générées !');
                console.log('💡 Vous pouvez maintenant comparer les qualités.');
            })
            .catch(console.error);
    } else {
        convertHtmlToPdfHighQuality()
            .then(() => {
                console.log('\n🏆 Version HAUTE QUALITÉ générée avec succès !');
            })
            .catch(console.error);
    }
}

module.exports = { convertHtmlToPdfHighQuality, generateQualityComparison };
