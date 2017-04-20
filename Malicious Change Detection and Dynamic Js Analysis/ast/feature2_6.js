var fs = require('fs'),
    esprima = require('esprima'),
    files = process.argv.splice(2);


files.forEach(function (filename) {
    var content = fs.readFileSync(filename, 'utf-8'),
        escapeCount = 0;
        unescapeCount = 0;
		evalCount = 0;
        keywordCount = 0;
        string_ = 0;
        count_identifier = 0;
	var tokens;
	try{
		var tokens = esprima.parse(content, { tokens: true }).tokens;
 
    tokens.forEach(function (token) {
        if (token.type === 'Identifier') {
            count_identifier++;

            if (token.type === 'Identifier' && token.value === 'eval' ) {
                evalCount++;
            // console.log(token.value);
                }
            else if (token.type === 'Identifier' && token.value === 'escape') {
                escapeCount++;
           // console.log(token.value);
            }
            else if (token.type === 'Identifier' && token.value === 'unescape') {
                unescapeCount++;
           // console.log(token.value);
            }
        }
        
       else if (token.type === 'Keyword') {
            keywordCount++;
            // console.log(token.value);
        }
        else if (token.type === 'String') {
           string_++;
       // else if (node.type === 'UnaryExpression' && token.value === '+') {
       //     iframeCount++;
       //     console.log(token.value);
       // }
    }});
	var ratio = keywordCount / string_;
	var ratio2 = keywordCount / count_identifier;
    console.log(ratio);
    console.log(ratio2);
    console.log(evalCount);
    console.log(escapeCount);
			  console.log(unescapeCount);
			  } catch(e){
			  console.log(-1);
			  console.log(-1);
			  console.log(-1);
			  console.log(-1);
			  console.log(-1);
			  }
    // console.log("iframeCount:" +iframeCount);
});




// var tokens = esprima.parse(script, { tokens: true }).tokens;
// var identifierCount = 0;
// var keywordCount = 0;

// tokens.forEach(function (token) {
//     if (token.type === 'Keyword') {
//         keywordCount++;
//     }
//     else if (token.type === 'Identifier') {
//         identifierCount++;
//     }
// });

// var ratio = keywordCount / identifierCount
