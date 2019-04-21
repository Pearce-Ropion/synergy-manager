import pandas as pd
import pickle
from sklearn import svm
from sklearn.preprocessing import StandardScaler

def gen_alert_model(chID, vals):
    X_train = pd.read_json(vals, typ='frame')
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    scl = StandardScaler() #normalize features individually so that mean = 0 and std = 1

    clf.fit(scl.fit_transform(X_train.as_matrix()))
    with open('./svms/' + chID + '.pickle', 'wb') as handle:
        pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

def pred_alert(chID, clf, test):
    with open('./svms/' + chID + '.pickle', 'rb') as handle:
        clf = pickle.load(handle)
    outliers = clf.predict(test)
    if outliers[0] == -1:
        gen_alert(chID)

def gen_alert(chID):
    print("ALERT for " + chID)
