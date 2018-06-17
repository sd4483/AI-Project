# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 17:56:57 2018

@author: sudhe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv('data.csv')
X = dataset.iloc[:,:-1].values
y = dataset.iloc[:,-1].values

X_missing_values = X.isnull().sum()
X.Symptom1 = X.Symptom1.fillna('Not defined')
X.Symptom2 = X.Symptom2.fillna('Not defined')
X.Symptom3 = X.Symptom3.fillna('Not defined')
X.Symptom4 = X.Symptom4.fillna('Not defined')
X.Symptom5 = X.Symptom5.fillna('Not defined')
X.Symptom6 = X.Symptom6.fillna('Not defined')
X.Symptom7 = X.Symptom7.fillna('Not defined')



encode_gender=pd.get_dummies(X['Gender'], prefix='Gender')
encode_nationality = pd.get_dummies(X['Nationality'], prefix = 'Nationality')
encode_symptom1 = pd.get_dummies(X['Symptom1'], prefix = 'Symptom1')
encode_symptom2 = pd.get_dummies(X['Symptom2'], prefix = 'Symptom2')
encode_symptom3 = pd.get_dummies(X['Symptom3'], prefix = 'Symptom3')
encode_symptom4 = pd.get_dummies(X['Symptom4'], prefix = 'Symptom4')
encode_symptom7 = pd.get_dummies(X['Symptom7'], prefix = 'Symptom7')
encode_symptom6 = pd.get_dummies(X['Symptom6'], prefix = 'Symptom6')
encode_symptom5 = pd.get_dummies(X['Symptom5'], prefix = 'Symptom5')
encode_disease = pd.get_dummies(y['Predicted_Disease'], prefix = 'Predicted_Disease')

#Encoding Categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder           #importing LabelEncoder and OneHotEncoder class from preprocessing lib in scikit

labelencoder_x = LabelEncoder()    #Encoding the categorical values with numbers in the first column
X[:, 0,2,3,4,5,6,7,8,9] = labelencoder_x.fit_transform(X[:, 0,2,3,4,5,6,7,8,9])
onehotencoder = OneHotEncoder(categorical_features = [0])               #Further diving the categorical values into 3 groups to eliminate order between the values
X = onehotencoder.fit_transform(X).toarray()

labelencoder_purchased = LabelEncoder()                                 #doing the same thing for dependent variable
y = labelencoder_purchased.fit_transform(Y)

