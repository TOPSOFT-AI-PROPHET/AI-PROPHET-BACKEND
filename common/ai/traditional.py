import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier


# Get train and test data from dataset
def preprocess(dataset, split):
    df = pd.read_csv(dataset)
    # Get feature and target values
    y = df.iloc[:, -1]
    X = df.iloc[:, :-1]
    # Split into train and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=split, random_state=1)
    return X_train, X_test, y_train, y_test


# Get best regression model given training data
def train_regressor(dataset, split):
    X_train, X_test, y_train, y_test = preprocess(dataset, split)
    rfr = RandomForestRegressor()
    n_estimators = [int(x) for x in np.linspace(start=100, stop=500, num=5)]
    max_depth = [int(x) for x in np.linspace(10, 50, num=5)]
    max_depth.append(None)
    bootstrap = [True, False]
    param_grid = {"n_estimators": n_estimators, "max_depth": max_depth, "bootstrap": bootstrap}
    g_search = GridSearchCV(estimator=rfr, param_grid=param_grid, cv=10, verbose=0, n_jobs=-1)
    g_search.fit(X_train, y_train)
    return g_search.best_estimator_


# Get best classification model given training data
def train_classifier(dataset, split):
    X_train, X_test, y_train, y_test = preprocess(dataset, split)
    rfc = RandomForestClassifier()
    n_estimators = [int(x) for x in np.linspace(start=100, stop=500, num=5)]
    max_depth = [int(x) for x in np.linspace(10, 50, num=5)]
    max_depth.append(None)
    bootstrap = [True, False]
    param_grid = {"n_estimators": n_estimators, "max_depth": max_depth, "bootstrap": bootstrap}
    g_search = GridSearchCV(estimator=rfc, param_grid=param_grid, cv=10, verbose=0, n_jobs=-1)
    g_search.fit(X_train, y_train)
    return g_search.best_estimator_
