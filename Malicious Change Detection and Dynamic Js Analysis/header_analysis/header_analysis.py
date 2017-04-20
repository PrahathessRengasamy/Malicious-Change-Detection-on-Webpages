import sys, json

if len(sys.argv) < 2:
	print 'usage header_analysis.py header_data.json'

header_list = ["content-security-policy", "content-security-policy-report-only", "x-webkit-csp", "x-content-security-policy", "public-key-pins", "public-key-pins-report-only", "x-content-type-options", "x-frame-options", "x-xss-protection", "x-download-options", "x-permitted-cross-domain-policies", "access-control-allow-origin"]
with open(sys.argv[1]) as json_file:
	json_data = json.load(json_file)
result = []
for each in json_data:
	score = 0
	site = {}
	site["url"] = each["URL"] 
	given_headers = map(str.lower, map(str, each["Headers"].keys()))
	for hd in header_list:
		if hd in given_headers:
			score += 1
	site["score"] = score
	result.append(site)

with open("headers.json", "w") as f:
	my_json_str = json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)
	f.write(my_json_str)	 
