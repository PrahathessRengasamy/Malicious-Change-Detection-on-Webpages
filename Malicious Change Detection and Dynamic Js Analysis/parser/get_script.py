from bs4 import BeautifulSoup
import sys, io, json, codecs

if len(sys.argv) < 2:
	print 'usage: python get_script.py html_code.txt'
	sys.exit()

with open(sys.argv[1]) as f:
	data = f.read()
script = ""
soup = BeautifulSoup(data, "html.parser")
for each in soup.findAll('script'):
	if len(each.contents) > 0: 
		script += each.contents[0]
		script = script.replace('\r', '').replace('\t', '')	
list_data = [{"script":script}]
with io.open("tmp_script.json", 'w', encoding='utf-8') as of:
	my_json_str = json.dumps(list_data, indent=4, sort_keys=True, ensure_ascii=False)
	my_json_str = my_json_str.encode('ascii', 'ignore').decode('ascii')
	my_json_str = codecs.decode(my_json_str, 'unicode_escape')
	of.write(my_json_str)