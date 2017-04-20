from bs4 import BeautifulSoup
import sys, io, json, codecs

if len(sys.argv) < 2:
	print 'usage: python' + sys.argv[0] + ' json_file.json'
	sys.exit()

with open(sys.argv[1]) as json_file:
	json_data = json.load(json_file)

list_data = []
for data in json_data:
	script = ""
	site = {}
	bd = []
	site["Rank"] = data["Rank"]
	soup = BeautifulSoup(data["Body"], "html.parser")
	for each in soup.findAll('html'):
		if len(each.contents) > 0: 
			body = each.contents[0]
			body = body.replace('\r', '').replace('\t', '')
			bd.append(body)
	site["Body"] = bd
	list_data.append(site)
with io.open("scripts.json", 'w', encoding='utf-8') as of:
	my_json_str = json.dumps(list_data, indent=4, sort_keys=True, ensure_ascii=False)
	#my_json_str = my_json_str.encode('ascii', 'ignore').decode('ascii')
	#my_json_str = codecs.decode(my_json_str, 'unicode_escape')
	of.write(my_json_str)
