# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 17:26:50 2018
Title: Data Preprocessing
@author: sudhe
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#Importing dataset
dataset = pd.read_csv("Data.csv")
X = dataset.iloc[:,:-1].values                                          #matrix of features(independent variables)
Y = dataset.iloc[:,3].values                                            #dependent vector

#Missing Values
from sklearn.preprocessing import Imputer                               #importing Imputer class from preprocessing lib in scikit

imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)  #dealing with missing values
imputer = imputer.fit(X[:, 1:3])                                        #fitting the above imputer object to X, 1:3 means, the columns 1 and 2 are selected
X[:, 1:3] = imputer.transform(X[:, 1:3])                                #This is where the actual missing values are being replaced by mean of the columns

#Encoding Categorical data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder           #importing LabelEncoder and OneHotEncoder class from preprocessing lib in scikit

labelencoder_country = LabelEncoder()                                   #Encoding the categorical values with numbers in the first column
X[:,0] = labelencoder_country.fit_transform(X[:,0])
onehotencoder = OneHotEncoder(categorical_features = [0])               #Further diving the categorical values into 3 groups to eliminate order between the values
X = onehotencoder.fit_transform(X).toarray()

labelencoder_purchased = LabelEncoder()                                 #doing the same thing for dependent variable
Y = labelencoder_purchased.fit_transform(Y)

#Splitting the dataset into training and test set
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0) #X and Y are arrays here, test_size 0.2 means 20%, and random_state is just a random number

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)



