from bs4 import BeautifulSoup
import urlparse
import sys, urllib, json

if len(sys.argv) != 2:
	print 'usage: python ' + sys.argv[0] + 'urls_txt_file'
	sys.exit()
with open(sys.argv[1], 'r') as f:
	lines = f.readlines()
base_url = "http://www.alexa.com/topsites/category/Top/"
for line in lines:
	url = base_url + line.rstrip() + '/'
	print url
	soup = BeautifulSoup(urllib.urlopen(url), "html.parser")
	result = set()
	for each in soup.findAll('a',href=True):
		href = each['href']
		if href.startswith("/siteinfo/") and len(href.replace("/siteinfo/", "")) > 0:
			parsed_uri = each.string.lower().split('/')[0]
			result.add(parsed_uri)
	with open('tmp_categorised.txt', 'a') as of:
		res = '\n'.join(list(result))
		of.write(res)
