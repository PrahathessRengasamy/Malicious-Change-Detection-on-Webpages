import re
#x = "var a = 2; c = 4"
#print x.split(' ')

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

#print get_words(x)
def get_feature_1(x):
    words = get_words(x)
    num_of_key = 0;
    for w in words:
        if w in keywords:
            num_of_key = num_of_key + 1;
    print num_of_key
    return float(num_of_key)/ float(len(words)-num_of_key)
#print get_feature_1(x)

def get_feature_2(x, th):
    type = -1
    temp = ''
    result = 0;
    counter = 0;
    for i in range(len(x)):
        if type == -1:
            if x[i] == '"':
                type = 1
            if x[i] == "'":
                type = 2;
        else:
            if (type == 1 and x[i] == '"' and x[i-1] != '\\') or (type == 2 and x[i] == "'" and x[i-1] != '\\') :
                if counter >= th:
                    result = result + 1
                counter = 0
                type = -1
            else:
                counter = counter + 1
    return result

#print get_featrue_2("\"aaaa\" '22'", 2)

import json
with open('../data/scripts.json') as data_file:
    data = json.load(data_file)
for d in data:
    script = d[u'Script'][0]
    print get_feature_1(script), get_feature_2(script, 40)
