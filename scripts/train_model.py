# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 08:28:15 2023

@author: Edgar David

This script is used to train a lasso model as same as in R code
"""

# Import libraries
# Imputation
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
# Utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Metrics
from sklearn.metrics import confusion_matrix , f1_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, roc_auc_score , precision_recall_curve, average_precision_score , accuracy_score
# Data splitting
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import StratifiedKFold
# model
from sklearn.linear_model import LogisticRegression , LogisticRegressionCV
print('Libraries loaded')

# Load data
df = pd.read_excel(r'D:\Escritorio\ASESORIAS\UpWork\Vincent_Ochs\Caret\app\data\DATA_COMPLETE_New.xlsx')
TARGET = ['ai']
print('NAN values per column:')
print(df.isnull().sum())
# Perform MICE imputation to height and weight
print('Performing imputation...')
# Split the data and impute the information
df_class_0 = df[df[TARGET[0]] == 0]
df_class_1 = df[df[TARGET[0]] == 1]
num_columns = ['height' , 'weight']
cat_columns = ['nutrition']

# Impute information
categorical_imputer = SimpleImputer(strategy = 'most_frequent')
df_class_0[cat_columns] = categorical_imputer.fit_transform(df_class_0[cat_columns])
numerical_imputer = IterativeImputer(imputation_order = 'ascending',
                                     max_iter = 500,
                                     random_state = 42,
                                     n_nearest_features = 10)
df_class_0[num_columns] = numerical_imputer.fit_transform(df_class_0[num_columns])

categorical_imputer = SimpleImputer(strategy = 'most_frequent')
df_class_1[cat_columns] = categorical_imputer.fit_transform(df_class_1[cat_columns])

numerical_imputer = IterativeImputer(imputation_order = 'ascending',
                                     max_iter = 500,
                                     random_state = 42,
                                     n_nearest_features = 10)
df_class_1[num_columns] = numerical_imputer.fit_transform(df_class_1[num_columns])
# Concat information
df = pd.concat([df_class_0,
                df_class_1] , axis = 0)
# Train Lasso model
print('Training Model..')
# Define functions for evaluation metrics
def calculate_confusion_matrix(true_labels, predicted_labels):
    # Calculate confusion matrix
    tn, fp, fn, tp = confusion_matrix(true_labels, predicted_labels).ravel()

    return tn, tp, fp, fn

def get_metrics(TN,TP,FP,FN):

    acc = (TN+TP)/(TN+TP+FN+FP)
    precision = TP / (TP + FP)

    # Calculate recall
    recall = TP / (TP + FN)
    # Calulcate specificity
    specificity = TN / (TN + FP)

    # Calculate F1 score
    f1 = 2 * (precision * recall) / (precision + recall)

    return acc, precision, recall, f1 , specificity
skf = RepeatedStratifiedKFold(n_splits = 10 ,
                              n_repeats = 50 ,
                              random_state = 1234)
X = df.drop(columns = TARGET)
Y = df[TARGET]


model = LogisticRegressionCV(penalty = 'l1',
                             cv = skf,
                             Cs = int(1 / 0.1),
                             solver = 'liblinear',
                             verbose = 1)
model.fit(X , Y)
predictions = model.predict(X)