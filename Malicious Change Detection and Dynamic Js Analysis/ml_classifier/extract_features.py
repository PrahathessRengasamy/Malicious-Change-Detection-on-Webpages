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

keywords = ['break', 'do',        'instanceof',  'typeof',
'case',      'else',      'new',         'var',
'catch',     'finally',   'return',      'void',
'continue',  'for'  ,     'switch',      'while',
'debugger',  'function',  'this' ,       'with',
'default',   'if' ,       'throw',
'delete',    'in',        'try]',
'abstract',  'export'   ,   'interface' , 'static',
'boolean',   'extends'  ,   'long'    ,   'super',
'byte'   ,   'final'    ,  'native'   ,  'synchronized',
'char'   ,   'float'       'package'  , 'throws',
'class'  ,   'goto'      ,  'private' ,   'transient',
'const'  ,   'implements' , 'protected' , 'volatile',
'double' ,   'import'   ,   'public' ,
'enum'   ,  'int'     ,    'short', 'null', 'true', 'false']

suspicious_tags = ['script', 'object', 'embed', 'frame' ]
suspicious_strs = [['evil', 'shell', 'spray', 'crypt'], ['clearAttributes', 'insertAdjacentElement', 'replaceNode'], ['decodeURIcomponent'], ['setTimeOut'], ['exec'], ['applet', 'script']]

def get_words(x):
    temp = ''
    result = []
    for i in range(len(x)):
        if x[i].isalnum():
            temp = temp + x[i]
        elif len(temp) > 0:
            result.append(temp)
            temp = ''
    result.append(temp)
    return result

def get_entropy(x):
    num_of_chars = dict()
    for c in x:
        if not c.isalnum():
            continue
        if c not in num_of_chars.keys():
            num_of_chars[c] = 0
        num_of_chars[c] += 1
    H = 0.0
    for k in num_of_chars.keys():
        p = float(num_of_chars[k]) / len(x)
        H += - p * np.log(p)
    return H

def get_feature_1(x):
    words = get_words(x)
    num_of_key = 0
    number_of_sus_strs = [0] * len(suspicious_strs)
    for w in words:
        if w in keywords:
            num_of_key = num_of_key + 1
        for i in range(len(suspicious_strs)):
            if w in suspicious_strs[i]:
                number_of_sus_strs[i] += 1
        if w in suspicious_strs:
            number_of_sus_strs = number_of_sus_strs + 1
    return float(num_of_key)/ float(len(words)-num_of_key), number_of_sus_strs

def get_feature_2(x, th):
    type = -1
    num_of_long_strs = 0;
    num_of_sus_tags = 0;
    num_of_iframes = 0;
    counter = 0;
    for i in range(len(x)):
        if type == -1:
            if x[i] == '"':
                type = 1
            if x[i] == "'":
                type = 2
        else:
            if (type == 1 and x[i] == '"' and x[i-1] != '\\') or (type == 2 and x[i] == "'" and x[i-1] != '\\') :
                if counter >= th:
                    num_of_long_strs = num_of_long_strs + 1
                counter = 0
                type = -1
            else:
                counter = counter + 1
                for s in suspicious_tags:
                    if x[i:(i+len(s))] == s:
                        num_of_sus_tags = num_of_sus_tags + 1
                if x[i:(i+6)] == 'iframe':
                    num_of_iframes = num_of_iframes + 1
    return num_of_long_strs, num_of_sus_tags, num_of_iframes

def get_all_features_js(script, file = None):
    script.encode('utf-8')
    f1 = get_feature_1(script)
    f2 = get_feature_2(script, 40)
    if not file == None:
        file.write( str(f1[0]) + " " + str(f1[1][0]) + " " + str(f1[1][1]) + ' ' + str(f1[1][2]) + ' ' + str(f1[1][3]) + ' ' + str(f1[1][4]) + ' ' + str(f1[1][5]) + " " + str(f2[0]) + " " + str(f2[1]) + ' ' + str(f2[2]) +' ' + str(get_entropy(script))+'\n')
    #fname = 'temp' + '.js'
    #script = '\n'.join([x for x in script if "@context" not in x]).encode('utf-8')
    #tmpf = codecs.open(fname, 'w', 'utf-8')
    #tmpf.write(script)
    #tmpf.close()
    #cmd = 'node feature1.js ' + fname
    #os.system(cmd)
    #cmd = 'node feature2_6.js ' + fname + '; rm ' + fname
    #os.system(cmd)
    return f1[0],f1[1][0], f1[1][1], f1[1][2], f1[1][3],f1[1][4],f1[1][5],f2[0],f2[1], f2[2], get_entropy(script)

def read_file(path):
    num_features = 11
    f = open(path)
    all_features = []
    while 1:
        line = f.readline()
        if not line:
            break
        features = line.split()
        for feature in features:
            if feature == 'false':
                feature = '0'
            elif feature == 'true':
                feature = '1'
            elif feature == 'NaN':
                feature = -1
            elif feature == 'Infinity':
                feature = -2
            all_features.append(float(feature))
    N = len(all_features)/ num_features
    X = np.zeros([N, num_features])

    for i in range(N):
        for j in range(num_features):
            X[i, j] = all_features[i*num_features + j]
    return N, X

#crawled_data_path = '/Users/mehrdad/day1.json'

if len(sys.argv) >= 2:
    day = sys.argv[1]
else:
    day = '1'

crawled_data_path = 'day' + day + '.json'

#extracting html features
os.system('go get golang.org/x/net/html')
os.system('go get golang.org/x/net/html/atom')
os.system('go run html_features.go 0 '  + crawled_data_path + ' temp_html_features' + day + '.dat')

#reading crawled data
with open(crawled_data_path) as data_file:
    data = json.load(data_file)

#js and html static analysis
features = dict()
counter = 0
N, html_features = read_file('temp_html_features' + day + '.dat')
for d in data:
    counter += 1
    #print d[u'URL']
    #if counter == 10:
    #    break
    if counter % 10 == 0:
        print 'feature extraction/day' + day + ':' + str(counter) +'/' + str(len(data))
    soup = BeautifulSoup(d["Body"], "html.parser")
    all_scripts = (soup.findAll('script'))
    sc = []
    for each in all_scripts:
        if len(each.contents) > 0:
            script = each.contents[0]
            sc.append(script)
    script = '\n'.join(sc)
    features[d['URL']] = dict()
    features[d['URL']]['html'] = html_features[counter - 1, :]
    features[d['URL']]['js'] = np.array(get_all_features_js(script))
    #print results[d['URL']]['scores']

#saving results
with open('features' + day + '.pkl', 'w') as outfile:
   pickle.dump(features, outfile)
#my_json_str = json.dumps(results, indent=4, sort_keys=True, ensure_ascii=False)
#of = open('results.json', 'w')
#of.write(my_json_str)
