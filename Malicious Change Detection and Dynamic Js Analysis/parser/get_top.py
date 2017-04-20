from bs4 import BeautifulSoup
import urllib2, csv, sys, json, httplib

website_data = {}
with open(sys.argv[1], 'r') as csv_file, open('log.txt', 'a') as log:
	top_reader = csv.reader(csv_file, delimiter=',')
	for row in top_reader:
		rank, wbtk = row[0], row[1]
		wbst = 'http://' + wbtk
		try:
			soup = BeautifulSoup(urllib2.urlopen(wbst), 'html.parser', from_encoding="iso-8859-1")
			log.write('[SUCCESS]: {rank}, {wbtk}'.format(rank=rank, wbtk=wbtk))
		except IOError, TypeError:
			log.write('[ERROR]: {rank} {wbtk}'.format( rank=rank, wbtk=wbtk ))
		except urllib2.HTTPError:
			log.write('[ERROR]: {rank} {wbtk}'.format( rank=rank, wbtk=wbtk ))
		except urllib2.URLError:
			log.write('[ERROR]: {rank} {wbtk}'.format( rank=rank, wbtk=wbtk ))
		except httplib.BadStatusLine, httplib.HTTPException:
			log.write('[ERROR]: {rank} {wbtk}'.format( rank=rank, wbtk=wbtk ))
		except Exception:
			log.write('[ERROR]: {rank} {wbtk}'.format( rank=rank, wbtk=wbtk ))
		#print rank, soup
		website_data[wbtk] = {'Rank': rank, 'Body':soup.findAll('html')}

with open('top_sample.json','w') as jf:
	my_json_str = json.dumps(website_data, indent=4, sort_keys=True, ensure_ascii=False)
	jf.write(my_json_str)
