var fs = require('fs');
var esvalid = require("esvalid");
var esprima = require('esprima');

var contents = fs.readFileSync(process.argv[2], 'utf-8');
var concatCount = 0;
	
	try{
		esprima.parse(contents, {}, function (node, meta) {
		  if (node.operator==='+') {
		    concatCount++;
		    // console.log('Ternary at line', meta.start.line);
		  	}	
			})
		
		console.log(concatCount);
		}
	catch(e)
	{
	//console.log(e);
	console.log(-1);
	}


;
