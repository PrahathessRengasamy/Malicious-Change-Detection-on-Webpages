var fs = require('fs'),
    esprima = require('esprima'),
    files = process.argv.splice(2);


files.forEach(function (filename) {
    var content = fs.readFileSync(filename, 'utf-8'),
        tokens = esprima.parse(content, { tokens: true }).tokens;
 
    tokens.forEach(function (token) {
        if (token.type === 'Keyword') {
            // console.log(token.value);
            console.log(files);
        }
    });
});

// function analyzeCode(code) {
// //    var ast = esprima.parse(code);

//     tokens = esprima.parse(code, { tokens: true }).tokens;
 
//     tokens.forEach(function (token) {
//         if (token.type === 'Keyword') {
//             console.log(token.value);
//         }
//     });


//     //console.log(JSON.stringify(ast, null, 4))
// }







// if (process.argv.length < 3) {
//     console.log('Usage: analyze.js file.js');
//     process.exit(1);
// }

// var filename = process.argv[2];
// console.log('Reading ' + filename);
// var code = fs.readFileSync(filename, 'utf-8');

// analyzeCode(code);
//console.log('Done');
 


