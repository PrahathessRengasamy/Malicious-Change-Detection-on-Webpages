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

start = 1
finish = 7
num_of_days = 7

if len(sys.argv) >= 2:
    start = int(sys.argv[1])
    finish = int(sys.argv[2])

for i in range(start-1, finish):
    day = str(i+1)
    os.system('python extract_features.py ' + day)
    os.system('python find_scores.py ' + day)
