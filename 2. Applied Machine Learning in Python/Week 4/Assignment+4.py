
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
# 
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
# 
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)). 
# 
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
# 
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
# 
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
# 
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
# 
# ___
# 
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
# 
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
# 
# <br>
# 
# **File descriptions** (Use only this data for training your model!)
# 
#     readonly/train.csv - the training set (all tickets issued 2004-2011)
#     readonly/test.csv - the test set (all tickets issued 2012-2016)
#     readonly/addresses.csv & readonly/latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC). 
# 
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
# 
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `readonly/train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `readonly/test.csv` will be paid, and the index being the ticket_id.
# 
# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#        
# ### Hints
# 
# * Make sure your code is working before submitting it to the autograder.
# 
# * Print out your result to see whether there is anything weird (e.g., all probabilities are the same).
# 
# * Generally the total runtime should be less than 10 mins. You should NOT use Neural Network related classifiers (e.g., MLPClassifier) in this question. 
# 
# * Try to avoid global variables. If you have other functions besides blight_model, you should move those functions inside the scope of blight_model.
# 
# * Refer to the pinned threads in Week 4's discussion forum when there is something you could not figure it out.

# In[13]:

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, auc, roc_curve
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import LabelEncoder

def blight_model():
     # Your code here
    #1. load the data
    train_data = pd.read_csv('train.csv', encoding = "ISO-8859-1")
    test_data = pd.read_csv('test.csv', encoding = "ISO-8859-1")
    
    #print(train_data.columns)
    #print(len(train_data.columns))
    
    #print(test_data.columns)
    #print(len(test_data.columns))
    
    #print(train_data.shape)
    #print(test_data.shape)
    
    #print("Count null values in train...")
    #print(train_data.isnull().sum())
    #print("Count null values in test...")
    #print(test_data.isnull().sum())
    
    #drop rows which contain null values of target
    train_data.dropna(axis = 0, subset = ['compliance'], inplace = True)
    #test_data.dropna(axis = 0, subset = ['disposition'], inplace = True)
    #print(len(train_data['agency_name'].unique()))
    #print(len(test_data['agency_name'].unique()))
    
    #drop unnecessary columns in train data
    train_data.drop(['ticket_id', 'violation_zip_code', 'non_us_str_code', 'grafitti_status', 'collection_status', 'compliance_detail', 'payment_amount', 
                     'balance_due', 'payment_date', 'payment_status', 'collection_status', 'violation_description', 'mailing_address_str_number', 
                     'mailing_address_str_name', 'ticket_issued_date', 'hearing_date', 'country', 'zip_code', 'state', 'city', 'violation_street_name', 'inspector_name', 'violator_name', 'disposition'], axis = 1, inplace = True)
    test_data.drop(['violation_zip_code', 'non_us_str_code', 'grafitti_status', 'violation_description', 'mailing_address_str_number', 'mailing_address_str_name', 
                    'ticket_issued_date', 'hearing_date', 'country', 'zip_code', 'state', 'city', 'violation_street_name', 'inspector_name', 'violator_name', 'disposition'], axis = 1, inplace = True)
    
    test_data.set_index('ticket_id', inplace = True)
    
    #print(train_data.columns)
    #print(len(train_data.columns))
    
    #print(test_data.columns)
    #print(len(test_data.columns))
    
    #print(train_data.shape)
    #print(test_data.shape)
    
    #print("Count null values in train...")
    #print(train_data.isnull().sum())
    #print("Count null values in test...")
    #print(test_data.isnull().sum())

    #print(train_data['disposition'].dtype)
    #print(train_data['disposition'].unique())
    
    labelencoder = LabelEncoder()
    #labelencoder.fit(train_data['disposition'].append(test_data['disposition'], ignore_index = True))
    #train_data['disposition'] = labelencoder.fit_transform(train_data['disposition'])
    #test_data['disposition'] = labelencoder.fit_transform(test_data['disposition'])
    
    train_data['violation_code'] = labelencoder.fit_transform(train_data['violation_code'])
    test_data['violation_code'] = labelencoder.fit_transform(test_data['violation_code'])
    
    train_data['agency_name'] = labelencoder.fit_transform(train_data['agency_name'])
    test_data['agency_name'] = labelencoder.fit_transform(test_data['agency_name'])
        
    #print(train_data['disposition'].dtype)
    #print(len(train_data['violation_code'].unique()))
    #print(len(test_data['violation_code'].unique()))
    # print("unique countries ", len(train_data['country'].unique()))
    #print("unique countries ", len(test_data['country'].unique()))
    #print(len(train_data['zip_code'].unique()))
    #print(len(test_data['zip_code'].unique()))
    
    
    X_data = train_data.iloc[:,:-1]
    y_data = train_data.iloc[:, -1]
    
    #split the data
    X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, random_state = 0)
    
    #train the model
    clf = GradientBoostingClassifier(random_state = 0)    
    #clf.fit(X_train, y_train)
    
    # Use AUC-ROC metric for evaluation
    param_test = {'learning_rate':[0.0001, 0.001, 0.01, 0.1, 1],  'max_depth':[2, 3, 4, 5]}
    grid_clf_auc = GridSearchCV(estimator = clf, param_grid = param_test, scoring='roc_auc')
    grid_clf_auc.fit(X_train, y_train)
    
    #print('Grid best parameter ()')
    #print('Grid best parameter (max. accuracy): ', grid_clf_auc.best_params_)
    #print('Grid best score (accuracy): ', grid_clf_auc.best_score_)
    
    y_pred = grid_clf_auc.predict_proba(test_data)[:, 1]
    #test_data['compliance'] = y_pred
    
    return pd.Series(y_pred, index = test_data.index)
    #gsearch5.grid_scores_, gsearch5.best_params_, gsearch5.best_score_
    
    #Evaluate the model performance using accuracy 
    #print('Blight Dataset')
    #print('Accuracy of GBDT classifier on training set: {:.2f}'.format(clf.score(X_train, y_train)))
    #print('Accuracy of GBDT classifier on validation set(.score): {:.2f}'.format(clf.score(X_val, y_val)))
    #print('Accuracy of GBDT classifier on validation set(accuracy_score): {:.2f}'.format(accuracy_score(X_val, y_val)))
    
# Your answer here


# In[ ]:

blight_model()


# In[ ]:



