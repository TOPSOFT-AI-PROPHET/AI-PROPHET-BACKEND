"""
The task of the code is to apply random forest algorithm on the train4.csv data and give the predictions on demanded inputs
"""
import numpy as np
import pandas as pd
import matplotlib as plt
from numpy import mean
from numpy import std

from sklearn import metrics
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor


def Data_split(data:str,ratio:float, target:str):
    # Import the dataset
    # 287 data with 23 features and label named "weight"
    df = pd.read_csv(data)
    # Split dataset into features and target
    y = df[target]
    X = df.drop(target, axis=1)
    #data_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=1)
    print(X_train.shape,"\n",X_test.shape,"\n",y_train.shape,"\n",y_test.shape)
    return X_train, X_test, y_train, y_test

def my_Cross_Validation(X_train, y_train):
    # model set
    # Random Forest model
    ## can add more model such as SVM, Linear Regression with Rugularisation, Ensemble methods...
    model = RandomForestRegressor()

    # scores to evaluate
    scoring = ['neg_mean_squared_error', 'r2']
    # Cross Validation method
    cv = RepeatedKFold(n_splits=10, n_repeats=5, random_state=1)

    # hyperparameter space, 2 * 12 * 2 * 3 * 3 * 10 = 4320 settings here
    ## Can Self define more base on sklearn
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
    # Number of features to consider at every split
    max_features = ['auto', 'sqrt']
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap}
    #n_iter trades off runtime vs quality of the solution
    rf_random = RandomizedSearchCV(estimator = model, param_distributions = random_grid, n_iter = 100, cv = cv, verbose=2, random_state=1, n_jobs = -1)
    # Fit the random search model on training data set and print best parameters
    # it is refitted to whole train_data set by default
    best_rf = rf_random.fit(X_train, y_train)
    print(best_rf.best_params_)
    return best_rf.best_estimator_
#print result on 
def Evaluation(model, X_test, y_test):
    y_hat = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, y_hat)
    mse = mean_squared_error(y_test, y_hat)
    r2 = r2_score(y_test, y_hat)
    accuracy = 100*(1-mape)
    print("Random Forest Model Performance:")
    print('R2 = {:0.2f}%.'.format(r2))
    print('MSE = {:0.2f}%.'.format(mse))
    print('MAPE = {:0.2f}%.'.format(mape))
    print('Accuracy = {:0.2f}%.'.format(accuracy))



#whole composite of traditional ML
def Machine_Learning(data:str,ratio:float, target:str):
    X_train, X_test, y_train, y_test = Data_split(data, ratio, target)
    best_rf_estimator = my_Cross_Validation(X_train, y_train)
    Evaluation(best_rf_estimator, X_test, y_test)
    return best_rf_estimator

#predict with given model
def Model_prediction():
    model = Machine_Learning("train4.csv", 0.2, "weight")
    feature_val = pd.Series(list(np.ones(10)))
    result = model.predict(feature_val)
    return result

Model_prediction()