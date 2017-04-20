var fs = require('fs'),
    esprima = require('esprima');



function analyzeCode(code) {
    var ast = esprima.parse(code);
    console.log(JSON.stringify(ast, null, 4))
}





if (process.argv.length < 3) {
    console.log('Usage: analyze.js file.js');
    process.exit(1);
}

var filename = process.argv[2];
console.log('Reading ' + filename);
var code = fs.readFileSync(filename, 'utf-8');

analyzeCode(code);
//console.log('Done');
