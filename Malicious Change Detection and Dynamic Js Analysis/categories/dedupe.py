import pandas as pd

toclean = pd.read_csv('all_category.csv', names=['no','website'])
dedupe = toclean.drop_duplicates(subset=['website'])
dedupe.to_csv('deduped.csv')
