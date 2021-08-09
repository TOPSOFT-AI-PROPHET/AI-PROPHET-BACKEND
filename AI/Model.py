import numpy as np
from sklearn import *
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from math import log
import pandas as pd
import operator
import graphviz

data = pd.read_csv("train4.csv",header=None)

array_data = np.array(data)

x_data = array_data[1: , :data.shape[1]-1]
y_data = array_data[1: , data.shape[1]-1]

dtree = RandomForestClassifier(criterion='entropy', random_state=0,max_depth=20)
dtree.fit(x_data, y_data)
prediction = np.array([[2,2,2,1,5,1,2,5,3,5,1,1,1,6,1,2,1,1,1,1,1,2,1]])

dump(dtree, 'weight_predict.joblib')

print(dtree.predict(prediction))

