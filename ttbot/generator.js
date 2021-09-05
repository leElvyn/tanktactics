const puppeteer = require('puppeteer');
const fs = require('fs');

(async() => {    
    const browser = await puppeteer.launch();
    const page = await browser.newPage();    
    await page.setContent(fs.readFileSync('./ttmap/index.html', 'utf8'), {waitUntil: "load"}); 
    await page.screenshot({path: './screenshot.png'});
    await browser.close();    
    })();