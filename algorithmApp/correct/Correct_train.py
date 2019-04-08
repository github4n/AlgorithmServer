import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

if __name__ == "__main__":
    path = 'testdata.data'
    data = pd.read_csv(path, header=None)
    data[4] = pd.Categorical(data[4])
    x, y = np.split(data.values, (4,), axis=1)
    # print(x)
    # print(y)

    x_train, x_test, y_train, y_test = train_test_split(x, y.astype('int'), random_state=1, train_size=0.8)

    svm_model = svm.SVC(C=0.5, kernel='linear', decision_function_shape='ovr')
    # svm_model = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
    svm_model.fit(x_train, y_train.ravel())
    joblib.dump(svm_model, "train_model.m")