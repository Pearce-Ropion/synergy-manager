import pandas as pd
import pickle
from sklearn import svm

from .svm_handler import trim_time
from .send_sms import unusual_msg
from ..database.database import connectDB, closeDB
from ..reporter import reportError, isError

#from sklearn.preprocessing import StandardScaler

def gen_alert_model(chID, vals):
    X_train = pd.DataFrame(vals)
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.01)
    #scl = StandardScaler() #normalize features individually so that mean = 0 and std = 1

    #clf.fit(scl.fit_transform(X_train))
    clf.fit(X_train)
    with open('./synergy/svms/' + chID + '.pickle', 'wb') as handle:
        pickle.dump(clf, handle, protocol=pickle.HIGHEST_PROTOCOL)

def pred_alert(chID, test):
    with open('./synergy/svms/' + chID + '.pickle', 'rb') as handle:
        clf = pickle.load(handle)
    #data = trim_time(test)
    amps = test['amps']
    time = test['time']
    outliers = clf.predict([[amps, time]])
    if outliers[0] == -1:
        generate_alert(chID)


def generate_alert(chID):
    # get channel name
    try:
        conn, cursor = connectDB()
        query = ''' SELECT name FROM channels WHERE channelID = %s '''
        cursor.execute(query, chID)
        name = cursor.fetchall()
    except Exception as error:
        reportError('SQL Error: Unable to retrieve channel name', error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)
    unusual_msg(name[0])
