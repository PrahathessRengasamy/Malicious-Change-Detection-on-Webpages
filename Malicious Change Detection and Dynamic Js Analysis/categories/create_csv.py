import sys, csv

if len(sys.argv) != 3:
	print 'python ' + sys.argv[0] + 'url_list.txt category_name'
with open("all_category.csv", 'r+a') as all_of, open(sys.argv[2]+".csv", 'w') as cat, open(sys.argv[1], 'r') as f:
	lines = f.readlines()
	dedupe = set(lines)
	all_count = sum(1 for row in csv.reader(all_of))
	count = 0
    	all_csvwriter = csv.writer(all_of, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    	cat_csvwriter = csv.writer(cat, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

	for each in dedupe:
		all_count += 1
		count += 1
		all_csvwriter.writerow([all_count, each.rstrip()])
		cat_csvwriter.writerow([count, each.rstrip()])