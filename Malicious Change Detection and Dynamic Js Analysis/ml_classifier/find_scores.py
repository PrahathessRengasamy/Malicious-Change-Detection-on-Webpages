import json
from bs4 import BeautifulSoup
import subprocess, os, sys, codecs
import numpy as np
import pickle
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA

def read_file(path, num_of_features):
    f = open(path)
    all_features = []
    while 1:
        line = f.readline()
        if not line:
            break
        features = line.split()
        for feature in features:
            all_features.append(float(feature))
    N = len(all_features)/ num_of_features
    X = np.zeros([N, num_of_features])

    for i in range(N):
        for j in range(num_of_features):
            X[i, j] = all_features[i*num_of_features + j]
    return N, X

if len(sys.argv) >= 2:
    day = sys.argv[1]
else:
    day = '1'

if len(sys.argv) >= 3:
    html_classifier_name = sys.argv[2]
else:
    html_classifier_name = 'random forest'
if len(sys.argv) >= 4:
    js_classifier_name = sys.argv[3]
else:
    js_classifier_name = 'random forest'
if len(sys.argv) >= 5:
    dyn_classifier_name = sys.argv[4]
else:
    dyn_classifier_name = 'decision tree'

feature_file_path = 'features' + day + '.pkl'

with open(feature_file_path) as feature_file:
    features = pickle.load(feature_file)

#reading classifiers info
with open('html_classifiers.pkl') as html_classifier_file:
    html_classifiers = pickle.load(html_classifier_file)
def html_classifier(f):
    p = 0
    if hasattr(html_classifiers[html_classifier_name], 'predict_proba'):
        p = html_classifiers[html_classifier_name].predict_proba(np.array([f]))[0][1]
    else:
        p = html_classifiers[html_classifier_name].predict(np.array([f]))[0]
    return p

with open('js_classifiers.pkl') as js_classifier_file:
    js_classifiers = pickle.load(js_classifier_file)
def js_classifier(f):
    p = 0
    if hasattr(js_classifiers[js_classifier_name], 'predict_proba'):
        p = js_classifiers[js_classifier_name].predict_proba(np.array([f]))[0][1]
    else:
        p = js_classifiers[js_classifier_name].predict(np.array([f]))[0]
    return p

with open('dyn_classifiers.pkl') as dyn_classifier_file:
    dyn_classifiers = pickle.load(dyn_classifier_file)
def dyn_classifier(f):
    p = 0
    if hasattr(dyn_classifiers[dyn_classifier_name], 'predict_proba'):
        p = dyn_classifiers[dyn_classifier_name].predict_proba(np.array([f]))[0][1]
    else:
        p = dyn_classifiers[dyn_classifier_name].predict(np.array([f]))[0]
    return p

#js and html static analysis
results = dict()
counter = 0

for url in features.keys():
    counter += 1
    if counter % 10 == 0:
        print 'scoring/part 1/day' + day + ':' + str(counter) + '/' + str(len(features))
    results[url] = dict()
    results[url]['features'] = dict()
    results[url]['scores'] = dict()
    results[url]['features']['html'] = features[url]['html']
    results[url]['scores']['html'] = html_classifier(features[url]['html'])
    results[url]['features']['js'] = features[url]['js']
    results[url]['scores']['js'] = js_classifier(features[url]['js'])
    #print results[d['URL']]['scores']

counter = 0
with open('day' + day + '.json') as data_file:
    data = json.load(data_file)
N, X = read_file('day' + day +'.txt', 8)
for d in data:
    counter += 1
    if counter % 10 == 0:
        print 'scoring/part 2/day' + day + ':' + str(counter) + '/' + str(len(features))
    url = str(d[u'URL'])
    results[url]['features']['dyn'] = X[counter - 1, :]
    results[url]['scores']['dyn'] = dyn_classifier(results[url]['features']['dyn'])

#saving results
with open('results' + day + '.pkl', 'w') as outfile:
   pickle.dump(results, outfile)
