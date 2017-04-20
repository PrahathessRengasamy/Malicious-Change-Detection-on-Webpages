var funcparse = function (content) {

	var escapeCount = 0;
		unescapeCount = 0;
		evalCount = 0;
		keywordCount = 0;
		string_ = 0;
		count_identifier = 0;

	var concatCount = 0;
	try{
		esprima.parse(content, {}, function (node, meta) {
			if (node.operator==='+') {
				concatCount++;
				// console.log('Ternary at line', meta.start.line);
			}
		})

		console.log(concatCount);
	} catch(e){
		//console.log(e);
		console.log(-1);
	}


	var tokens;
	try{
		var tokens = esprima.parse(content, { tokens: true }).tokens;

		tokens.forEach(function (token) {
			if (token.type === 'Identifier') {
				count_identifier++;

				if (token.type === 'Identifier' && token.value === 'eval' ) {
					evalCount++;
					// console.log(token.value);
				} else if (token.type === 'Identifier' && token.value === 'escape') {
				escapeCount++;
				// console.log(token.value);
				} else if (token.type === 'Identifier' && token.value === 'unescape') {
				unescapeCount++;
				// console.log(token.value);
				}
			} else if (token.type === 'Keyword') {
				keywordCount++;
				// console.log(token.value);
			} else if (token.type === 'String') {
				string_++;
				// else if (node.type === 'UnaryExpression' && token.value === '+') {
				//     iframeCount++;
				//     console.log(token.value);
				// }
			}
		});
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
}


var fs = require('fs'),
esprima = require('esprima');

var mode = parseInt(process.argv[2]);

if (mode == 0){
	var files = process.argv.splice(3);
	files.forEach(function (filename){
		var content = fs.readFileSync(filename, 'utf-8');
		funcparse(content);
	});
} else if (mode == 1){
	console.log(process.argv[3]); 
	var content = fs.readFileSync(process.argv[3], 'utf-8');
	var obj = JSON.parse(content);
	
	obj.forEach(function(page){
		page.Script.forEach(function(content){
			console.log("\t\t\tRank: \t" + page.Rank);
			funcparse(content);
		});
	});
} else if (mode == 2){
	var files = fs.readdirSync(process.argv[3]);
	files.forEach(function (filename){
		//console.log(filename);
		var content = fs.readFileSync(process.argv[3]+filename, 'utf-8');
		funcparse(content);
	});
}













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
