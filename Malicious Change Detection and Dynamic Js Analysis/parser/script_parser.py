from bs4 import BeautifulSoup
import sys, io, json, codecs

if len(sys.argv) < 2:
	print 'usage: python script_parser.py json_file.json'
	sys.exit()

with open(sys.argv[1]) as json_file:
	json_data = json.load(json_file, encoding="ISO-8859-1")

list_data = []
for data in json_data:
	script = ""
	site = {}
	sc = []
	site["Rank"] = data["Rank"]
	soup = BeautifulSoup(data["Body"], "html.parser")
	all_scripts = soup.findAll('script')
	for each in all_scripts:
		if len(each.contents) > 0: 
			script = each.contents[0]
			script = script.replace('\r', '').replace('\t', '')
			sc.append(script)
	site["Script"] = sc
	list_data.append(site)
fn =  "top_sample_scripts.json" 
with io.open(fn, 'w', encoding='utf-8') as of:
	my_json_str = json.dumps(list_data, indent=4, sort_keys=True, ensure_ascii=False)
	#my_json_str = my_json_str.encode('ascii', 'ignore').decode('ascii')
	#my_json_str = codecs.decode(my_json_str, 'unicode_escape')
	of.write(my_json_str)
