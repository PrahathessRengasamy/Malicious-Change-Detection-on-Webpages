from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import json
import pickle
import matplotlib
import sys

def read_file(path, num_of_features):
    f = open(path)
    all_features = []
    while 1:
        line = f.readline()
        if not line:
            break
        features = line.split()
        for feature in features:
            if not float(feature) == -1.0:
                all_features.append(float(feature))
    N = len(all_features)/ num_of_features
    X = np.zeros([N, num_of_features])

    for i in range(N):
        for j in range(num_of_features):
            X[i, j] = all_features[i*num_of_features + j]
    return N, X

if len(sys.argv) >= 2:
    num_of_features = int(sys.argv[1])
    outname = sys.argv[2]
    N1, X1 = read_file(sys.argv[3], num_of_features)
    N2, X2 = read_file(sys.argv[4], num_of_features)
    titleplot = sys.argv[5]
else:
    num_of_features = 11
    outname = 'js_classifiers.pkl'
    N1, X1 = read_file('mj.dat', num_of_features)
    N2, X2 = read_file('bj.dat', num_of_features)
    titleplot = 'Static JS'

print 'Number of benign: ' + str(N2) + '/Number of malicious: ' + str(N1)
X = np.append(X1, X2, axis=0)
Y = np.append(np.ones(N1), np.zeros(N2))

#splitting data into training and testing
n_example = len(Y)
n_training = int(.8*n_example)
np.random.seed(2017)
training_id = np.random.choice(range(n_example), size=n_training, replace=False)
testing_id = list(set(range(n_example))-set(training_id))
x_training = X[training_id]
y_training = Y[training_id]
x_testing = X[testing_id]
y_testing = Y[testing_id]

#find type 1 and 2 errors
def get_ab(p, th):
    alpha = 0
    beta = 0
    n0 = 0
    n1 = 0
    for y in y_testing:
        if y == 0:
            n0 += 1
        else:
            n1 += 1
    for i in range(len(y_testing)):
        if y_testing[i] == 0 and p[i] >= th:
            alpha += 1
        if y_testing[i] == 1 and p[i] <= th:
            beta += 1
    return float(alpha) / n0, float(beta) / n1

def linear_regression_test():
    linear = linear_model.LinearRegression()
    linear.fit(x_training, y_training)
    linear.score(x_training, y_training)
    return linear.predict(x_testing), linear

def logistic_regression_test():
    model = LogisticRegression()
    model.fit(x_training, y_training)
    model.score(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def decision_tree_test():
    model = tree.DecisionTreeClassifier(criterion='gini')
    model.fit(x_training, y_training)
    model.score(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def svm_test():
    model = svm.SVC(probability=True)
    model.fit(x_training, y_training)
    model.score(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def naive_baysian_test():
    model = GaussianNB()
    model.fit(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def k_nearest_point_test():
    model = KNeighborsClassifier(n_neighbors=6)
    model.fit(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def kmeans_test():
    model = KMeans(n_clusters=2, random_state=0)
    model.fit(x_training)
    return model.predict(x_testing), model

def random_forest_test():
    model = RandomForestClassifier()
    model.fit(x_training, y_training)
    return model.predict_proba(x_testing)[:, 1], model

def PCA_test():
    pca = PCA(n_components=num_of_features)
    pca.fit(X)
    print pca.explained_variance_ratio_

############## Options to generate nice figures
fig_width_pt = 640.0  # Get this from LaTeX using \showthe\columnwidth
# fig_height_pt = 480.0
inches_per_pt = 1.0 / 72.27  # Convert pt to inch
golden_mean = (np.sqrt(5) - 1.0) / 2.0  # Aesthetic ratio
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * golden_mean  # height in inches
fig_size = [fig_width, fig_height]

my_yellow = [235. / 255, 164. / 255, 17. / 255]
my_blue = [58. / 255, 93. / 255, 163. / 255]
dark_gray = np.array([68, 84, 106]) / 255.0

my_color = dark_gray  # pick color for theme
params_keynote = {
    'axes.labelsize': 16,
    'font.size': 16,
    'legend.fontsize': 14,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'text.usetex': True,
    'text.latex.preamble': '\\usepackage{sfmath}',
    'font.family': 'sans-serif',
    'figure.figsize': fig_size
}
params_ieee = {
    'axes.labelsize': 14,
    'font.size': 14,
    'legend.fontsize': 12,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'text.usetex': True,
    # 'text.latex.preamble': '\\usepackage{sfmath}',
    'font.family': 'serif',
    'font.serif': 'ptm',
    'figure.figsize': fig_size
}
matplotlib.rcParams.update(params_ieee)
fid = plt.figure(outname)
fid.patch.set_alpha(0.0)

classifiers = [linear_regression_test, logistic_regression_test, decision_tree_test, svm_test, naive_baysian_test, k_nearest_point_test, kmeans_test, random_forest_test]
colors = ['red', 'black', 'green', 'yellow', 'gray', 'magenta', 'cyan', my_blue]
classifier_names = ['linear regression', 'logistic regression', 'decision tree', 'svm', 'naive baysian', 'k nearest point', 'kmeans', 'random forest']
classifier_names_capital = ['Linear Regression', 'Logistic Regression', 'Decision Tree', 'SVM', 'Naive Baysian', 'K Nearest Point', 'K Means', 'Random Forest']
plots = [None] * (len(classifiers) + 1)
PCA_test()
models = dict()
for c in range(len(classifiers)):
    p, m = classifiers[c]()
    models[classifier_names[c]] = m
    ths = np.arange(0, 1, .01)
    alpha =  np.array([None] * len(ths))
    beta = np.array([None] * len(ths))
    for i in range(len(ths)):
        r = get_ab(p, ths[i])
        alpha[i] = r[0]
        beta[i] = r[1]
    if c == 3:
        for i in range(len(alpha)):
            if alpha[i] <= 0.01:
                thsh = ths[i]
                break
        print 'threshold: ' + str(thsh)
    plt.plot(alpha, 1-beta, color = colors[c], hold = True, label=classifier_names_capital[c], linewidth = 1.5)
flip_coin_a = np.arange(0, 1, .01)
flip_coin_b = 1 - flip_coin_a
plt.grid(True, which='major', linestyle='--')
plt.plot(flip_coin_a, 1- flip_coin_b, 'b--',  hold=True, label = 'Blind Test', linewidth = .5)
plt.legend()
plt.xlabel('False Positive')
plt.ylabel('True Positive')
plt.yticks(np.arange(0, 1, 0.1))
plt.xticks(np.arange(0, 1, 0.1))
plt.title('ROC Curve for ' + titleplot + ' Analysis')
plt.ylim(-0.01, 1.01)
plt.xlim(-0.01, 1.01)
plt.show()

scores0 = []
scores1 = []
pr = models['random forest'].predict_proba(x_testing)
for i in range(len(y_testing)):
    if y_testing[i] == 0:
        scores0.append(pr[i][1])
    else:
        scores1.append(pr[i][1])
scores0 = np.array(scores0)
scores1 = np.array(scores1)

scores0 = np.sort(scores0)
scores1 = np.sort(scores1)
p0 = np.arange(0, 1, 1./len(scores0))
p1 = np.arange(0, 1, 1./len(scores1))
p0 = p0[:len(scores0)]
p1 = p1[:len(scores1)]

fid.patch.set_alpha(0.0)

plt.grid(True, which='major', linestyle='--')
plt.grid(True, which='minor', linestyle='-')

plt.plot(scores0, p0, color='blue', hold=True, label='Benign', linewidth=1.5)
plt.plot(scores1, p1, color='red', hold=True, label='Malicious', linewidth=1.5)
plt.xlabel('Score Value')
plt.ylabel('CDF')
plt.yticks(np.arange(0, 1, 0.1))
plt.xticks(np.arange(0, 1, 0.1))
plt.title('The CDF of the Classifier Output for ' + titleplot + ' Analysis')
plt.legend()
plt.show()
with open(outname, 'w') as outfile:
    pickle.dump(models, outfile)
