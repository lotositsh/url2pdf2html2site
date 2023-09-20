const fs = require('fs');
var savePageWE=require('./nodeSavePageWE');


const text = fs.readFileSync('text.txt', 'utf8');
const filename = fs.readFileSync('filename.txt', 'utf8');

const path = filename.trim() + '.html';
console.log(text);
savePageWE.scrape({ url: text, path: path, lazyload: false }).then(function () {
    console.log("ok");
});
