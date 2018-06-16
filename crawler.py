# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 17:56:57 2018

@author: sudhe
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv('data.csv')
X = dataset.iloc[:,:-1]
y = dataset.iloc[:,-1]

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
encode_symptom1
encode_synptom2