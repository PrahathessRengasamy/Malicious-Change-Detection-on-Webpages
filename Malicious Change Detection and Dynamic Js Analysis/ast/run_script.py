import subprocess, os, sys, json, codecs

if len(sys.argv) != 2:
	print 'usage ' + sys.argv[0] + 'scripts.json'
	sys.exit()

with open(sys.argv[1], 'r') as inf: 
	json_data = json.load(inf)
for each in json_data:
	fname = each['Rank'] + '.js'
	tmpf = open(fname, 'w') 
	script = each['Script']
	script = '\n'.join([x for x in script if "@context" not in x]).encode('utf-8')
	if len(script) < 100:
		continue
	tmpf.write(script)
	tmpf.close()
	cmd = 'node keywords.js ' + fname + ' | sort | uniq -c | sort -nr; rm ' + fname
	os.system(cmd)
