"""
The task of the code is to apply random forest algorithm on the train4.csv data and give the predictions on demanded inputs
"""

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
# from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
# from sklearn.model_selection import RepeatedKFold
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
import time

def test_func():
    print("Hello")

# def Data_split(data:str,ratio:float, target:str):
#     # Import the dataset
#     # 287 data with 23 features and label named "weight"
#     df = pd.read_csv(data)
#     # Split dataset into features and target
#     y = df[target]
#     X = df.drop(target, axis=1)
#     #data_split
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=1)
#     return X_train, X_test, y_train, y_test
def Data_split(data,ratio:float):
    # Import the dataset
    # 287 data with 23 features and label named "weight"
    df = pd.read_csv(data)
    # Split dataset into features and target
    y = df.iloc[:,-1]
    X = df.iloc[:,:-1]
    #data_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ratio, random_state=1)
    return X_train, X_test, y_train, y_test


def my_Cross_Validation(X_train, y_train):
    # model set
    # Random Forest model
    ## can add more model such as SVM, Linear Regression with Rugularisation, Ensemble methods...
    model = RandomForestRegressor()

    # scores to evaluate
    scoring = ['neg_mean_squared_error']
    # Cross Validation method
    # cv = RepeatedKFold(n_splits=10, n_repeats=5, random_state=1)
    cv = 10
    # hyperparameter space, 2 * 6 * 5 = 60 settings here
    ## Can Self define more base on sklearn
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 100, stop = 500, num = 5)]
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 50, num = 5)]
    max_depth.append(None)
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'bootstrap': bootstrap}
    #n_iter trades off runtime vs quality of the solution
    rf_random = GridSearchCV(estimator = model, param_grid = random_grid, cv = cv, verbose=2, n_jobs = -1)
    # Fit the random search model on training data set and print best parameters
    # it is refitted to whole train_data set by default
    rf_random.fit(X_train, y_train)
    #print(best_rf.best_params_)
    return rf_random.best_estimator_, rf_random.best_params_
# #print result on 
# def Evaluation(model, X_test, y_test):
#     y_hat = model.predict(X_test)
#     mape = mean_absolute_percentage_error(y_test, y_hat)
#     mse = mean_squared_error(y_test, y_hat)
#     r2 = r2_score(y_test, y_hat)
#     accuracy = 100*(1-mape)
#     print("Random Forest Model Performance:")
#     print('R2 = {:0.2f}'.format(r2))
#     print('MSE = {:0.2f}'.format(mse))
#     print('MAPE = {:0.2f}'.format(mape))
#     print('Accuracy = {:0.2f}%.'.format(accuracy))

def my_Cross_Validation_c(X_train, y_train):
    # model set
    # Random Forest model
    ## can add more model such as SVM, Linear Regression with Rugularisation, Ensemble methods...
    model = RandomForestClassifier()

    # scores to evaluate
    scoring = ['neg_mean_squared_error']
    # Cross Validation method
    # cv = RepeatedKFold(n_splits=10, n_repeats=5, random_state=1)
    cv = 10
    # hyperparameter space, 2 * 6 * 5 = 60 settings here
    ## Can Self define more base on sklearn
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start = 100, stop = 500, num = 5)]
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 50, num = 5)]
    max_depth.append(None)
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    # Create the random grid
    random_grid = {'n_estimators': n_estimators,
               'max_depth': max_depth,
               'bootstrap': bootstrap}
    #n_iter trades off runtime vs quality of the solution
    rf_random = GridSearchCV(estimator = model, param_grid = random_grid, cv = cv, verbose=2, n_jobs = -1)
    # Fit the random search model on training data set and print best parameters
    # it is refitted to whole train_data set by default
    rf_random.fit(X_train, y_train)
    #print(best_rf.best_params_)
    return rf_random.best_estimator_, rf_random.best_params_



#whole composite of traditional ML
def Machine_Learning(data:str,ratio:float):
    # starting time
    start = time.time()
    X_train, X_test, y_train, y_test = Data_split(data, ratio)
    best_rf_estimator, best_rf_params = my_Cross_Validation(X_train, y_train)

    # Evaluation(best_rf_estimator, X_test, y_test)
    # end time
    end = time.time()
    total_time = end - start
    # print("Your total training time is:"+str(total_time)+"sec\n" ,"Your best params are:",best_rf_params)
    #save model
    return best_rf_estimator

#whole composite of traditional ML - classification
def Machine_Learning_c(data:str,ratio:float):
    # starting time
    start = time.time()
    X_train, X_test, y_train, y_test = Data_split(data, ratio)
    best_rf_estimator, best_rf_params = my_Cross_Validation_c(X_train, y_train)

    # Evaluation(best_rf_estimator, X_test, y_test)
    # end time
    end = time.time()
    total_time = end - start
    # print("Your total training time is:"+str(total_time)+"sec\n" ,"Your best params are:",best_rf_params)
    #save model
    return best_rf_estimator

#predict with given model
def Model_prediction(input_ls:list, model_name:str):
    # model = Machine_Learning("train4.csv", 0.2, "weight")
    model = joblib.load(model_name)
    # feature_val = pd.Series(list(np.ones(10,1)))
    result = model.predict(input_ls.reshape(1,-1))
    # print("Your prediction is:"+str(result[0]))
    return result



