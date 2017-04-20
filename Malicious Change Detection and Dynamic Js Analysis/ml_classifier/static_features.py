import subprocess, os, sys, json, codecs
import numpy as np

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

def print_features(script, file):
    script.encode('utf-8')
    f1 = get_feature_1(script)
    f2 = get_feature_2(script, 40)
    #print type (f1[1]), len(f1[1]), str(f1[1][1])
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

#malicious scripts
os.system('ls mal_js>script_names')
script_names_file = open('script_names')
malicious_names = []
while 1:
    line = script_names_file.readline()
    if not line:
        break
    if line[-2] == '*':
        line = line[0:-2]
    else:
        line = line[0:-1]
    malicious_names.append(line)
script_names_file.close()

malicious_feature_file = open('mj.dat', 'w')
num_of_malicious = len(malicious_names)
#malicious_feature_file.write(str(num_of_malicious) + '\n')
for i in range(num_of_malicious):
    f1 = codecs.open('./mal_js/' + malicious_names[i], "r", "utf-8")
    script = f1.read()
    f1.close()
    script.encode('utf-8')
    print_features(script, malicious_feature_file)
malicious_feature_file.close()
#bening scripts
with open('scripts_benign.json') as data_file:
    data = json.load(data_file)
#num_of_benigns = 0
#for d in data:
#    if len(d[u'Script']) > 0:
#        num_of_benigns += 1
benign_feature_file = open('bj2.dat', 'w')
#benign_feature_file.write(str(num_of_benigns) + '\n')
for d in data:
    if len(d['Script']) > 0:
        script = d['Script']
        print_features(script, benign_feature_file)
