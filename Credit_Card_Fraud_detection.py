# -*- coding: utf-8 -*-
"""Final_Notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nHa_cK-pdDgVOfhF5Si0MN9EZW815ID9

Exploratory Data Analysis
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv(r'/content/drive/MyDrive/Credit Card Fraud Detection/creditcard.csv')
df.head()

df.describe().transpose()

var = df.columns.values

i = 0
t0 = df.loc[df['Class'] == 0]
t1 = df.loc[df['Class'] == 1]

sns.set_style('whitegrid')
plt.figure()
fig, ax = plt.subplots(8,4,figsize=(16,28))

for feature in var:
    i += 1
    plt.subplot(8,4,i)
    sns.kdeplot(t0[feature], bw=0.4,label="Class = 0")
    sns.kdeplot(t1[feature], bw=0.4,label="Class = 1")
    plt.xlabel(feature, fontsize=10)
    locs, labels = plt.xticks()
    plt.tick_params(axis='both', which='major', labelsize=10)
plt.show();

round(100 * (df.isnull().sum()/len(df)),2).sort_values(ascending=False).head()

df.shape

df.drop_duplicates(subset=None, inplace=True)
df.shape

plt.figure(figsize=(8,8))
plt.title('Transaction Time Distributions')
sns.distplot(df['Time'])
plt.show()

plt.figure(figsize = (14,14))
plt.title('Credit Card Transactions features correlation plot (Pearson)')
corr = df.corr()
sns.heatmap(corr,xticklabels=corr.columns,yticklabels=corr.columns,linewidths=.1,cmap="Reds")
plt.show()

plt.hist(np.log(df["Amount"] +1), bins=50)
plt.gca().set(title='Frequency Histogram', ylabel='Frequency');

df.Class.value_counts()
sns.countplot("Class",data=df)

fig, axs = plt.subplots(ncols=2, figsize=(16,4))

sns.distplot(df[(df['Class'] == 1)]['Time'], bins=100, color='red', ax=axs[0])
axs[0].set_title("Distribution of Fraud Transactions")

sns.distplot(df[(df['Class'] == 0)]['Time'], bins=100, color='green', ax=axs[1])
axs[1].set_title("Distribution of Genuine Transactions")

plt.show()

f, (ax1, ax2) = plt.subplots(1,2,figsize =( 18, 8))
corr = df.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
sns.heatmap((df.loc[df['Class'] ==1]).corr(), vmax = .8, square=True, ax = ax1, cmap = 'afmhot', mask=mask);
ax1.set_title('Fraud')
sns.heatmap((df.loc[df['Class'] ==0]).corr(), vmax = .8, square=True, ax = ax2, cmap = 'YlGnBu', mask=mask);
ax2.set_title('Non-Fraud')
plt.show()

"""Standardization """

# Scale amount by log
df['amount_log'] = np.log(df.Amount + 0.01)

#Scale amount by Standardization
from sklearn.preprocessing import StandardScaler 
ss = StandardScaler()
df['amount_scaled'] = ss.fit_transform(df['Amount'].values.reshape(-1,1))

#Scale amount by Normalization
from sklearn.preprocessing import MinMaxScaler
norm = MinMaxScaler()
df['amount_minmax'] = norm.fit_transform(df['Amount'].values.reshape(-1,1))

fig,axs = plt.subplots(nrows = 1 , ncols = 4 , figsize = (20,4))

sns.boxplot(x ="Class",y="Amount",data=df, ax = axs[0])
axs[0].set_title("Class vs Amount")

sns.boxplot(x ="Class",y="amount_log",data=df, ax = axs[1])
axs[1].set_title("Class vs Log Amount")

sns.boxplot(x ="Class",y="amount_scaled",data=df, ax = axs[2])
axs[2].set_title("Class vs Scaled Amount")

sns.boxplot(x ="Class",y="amount_minmax",data=df, ax = axs[3])
axs[3].set_title("Class vs Min Max Amount")

plt.show()

"""Sampling Methods """

from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler,SMOTE, ADASYN
from sklearn import metrics

X = df.drop(['Class','Amount','amount_minmax','amount_scaled','Time'],axis=1)
y = df['Class']

"""Random Under Sample Dataset"""

X_train, X_test, y_train, y_test=train_test_split(X,y,test_size=0.3, shuffle=True)

print("X_train: ",X_train.shape)
print("y_train: ",y_train.shape)
print("X_test: ",X_test.shape)
print("y_test: ",y_test.shape)

print('\n')
print('............')
print('\n')

rus= RandomUnderSampler(sampling_strategy='majority')
X_train_under,y_train_under=rus.fit_resample(X_train, y_train)
X_test_under, y_test_under = X_test, y_test

print("X_train_under: ",X_train_under.shape)
print("y_train_under: ",y_train_under.shape)
print("X_test_under: ",X_test_under.shape)
print("y_test_under: ",y_test_under.shape)

"""SMOTE Dataset"""

print("X_train: ",X_train.shape)
print("y_train: ",y_train.shape)
print("X_test: ",X_test.shape)
print("y_test: ",y_test.shape)

print('\n')
print('............')
print('\n')


smote= SMOTE(sampling_strategy='minority')
X_train_smote,y_train_smote=smote.fit_resample(X_train, y_train)
X_test_smote, y_test_smote = X_test, y_test

print("X_train_smote: ",X_train_smote.shape)
print("y_train_smote: ",y_train_smote.shape)
print("X_test_smote: ",X_test_smote.shape)
print("y_test_smote: ",y_test_smote.shape)

"""ADASYN Dataset"""

print("X_train: ",X_train.shape)
print("y_train: ",y_train.shape)
print("X_test: ",X_test.shape)
print("y_test: ",y_test.shape)

print('\n')
print('............')
print('\n')
 

adasyn= ADASYN(sampling_strategy='minority')
X_train_adasyn,y_train_adasyn=adasyn.fit_resample(X_train, y_train)
X_test_adasyn, y_test_adasyn = X_test, y_test

print("X_train_adasyn: ",X_train_adasyn.shape)
print("y_train_adasyn: ",y_train_adasyn.shape)
print("X_test_adasyn: ",X_test_adasyn.shape)
print("y_test_adasyn: ",y_test_adasyn.shape)

names=[]
aucs_tests = []
accuracy_tests = []
precision_tests = []
recall_tests = []
f1_score_tests = []

def performance(model):
    for name, model, X_train, y_train, X_test, y_test in model:
        
        #appending name
        names.append(name)
        
        # Build model
        model.fit(X_train, y_train)
        
        #predictions
        y_test_pred = model.predict(X_test)
        
        # calculate accuracy
        Accuracy_test = metrics.accuracy_score(y_test, y_test_pred)
        accuracy_tests.append(Accuracy_test)
        
        # calculate auc
        Aucs_test = metrics.roc_auc_score(y_test , y_test_pred)
        aucs_tests.append(Aucs_test)
        
        #precision_calculation
        Precision_score_test = metrics.precision_score(y_test , y_test_pred)
        precision_tests.append(Precision_score_test)
        
        # calculate recall
        Recall_score_test = metrics.recall_score(y_test , y_test_pred)
        recall_tests.append(Recall_score_test)
        
        #calculating F1
        F1Score_test = metrics.f1_score(y_test , y_test_pred)
        f1_score_tests.append(F1Score_test)
        
        # draw confusion matrix
        cnf_matrix = metrics.confusion_matrix(y_test, y_test_pred)
        
        print("Model Name :", name)
        print('Test Accuracy :{0:0.5f}'.format(Accuracy_test))
        print('Test AUC : {0:0.5f}'.format(Aucs_test))
        print('Test Precision : {0:0.5f}'.format(Precision_score_test))
        print('Test Recall : {0:0.5f}'.format(Recall_score_test))
        print('Test F1 : {0:0.5f}'.format(F1Score_test))
        print('Confusion Matrix : \n', cnf_matrix)
        print("\n")

        fpr, tpr, thresholds = metrics.roc_curve(y_test, y_test_pred)
        auc = metrics.roc_auc_score(y_test, y_test_pred)
        plt.plot(fpr,tpr,linewidth=2, label=name + ", auc="+str(auc))
    
    plt.legend(loc=4)
    plt.plot([0,1], [0,1], 'k--' )
    plt.rcParams['font.size'] = 12
    plt.title('ROC curve')
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.show()

"""Logical Regression Classifier"""

from sklearn.linear_model import LogisticRegression

LRmodel=[]

LRmodel.append(('LR IMBALANCED', LogisticRegression(solver='saga',multi_class='multinomial'),X_train, y_train, X_test, y_test))
LRmodel.append(('LR UNDERSAMPLE', LogisticRegression(solver='saga',multi_class='multinomial'),X_train_under, y_train_under, X_test_under, y_test_under))
#LRmodel.append(('LR OVERSAMPLE', LogisticRegression(solver='saga',multi_class='multinomial'),X_train_over, y_train_over, X_test_over, y_test_over))
LRmodel.append(('LR SMOTE', LogisticRegression(solver='saga',multi_class='multinomial'),X_train_smote, y_train_smote, X_test_smote, y_test_smote))
LRmodel.append(('LR ADASYN ', LogisticRegression(solver='saga',multi_class='multinomial'),X_train_adasyn, y_train_adasyn, X_test_adasyn, y_test_adasyn))

performance(LRmodel)

"""Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier

RFmodel = []

RFmodel.append(('RF IMABALANCED', RandomForestClassifier(),X_train,y_train,X_test,y_test))
RFmodel.append(('RF UNDERSAMPLE', RandomForestClassifier(),X_train_under, y_train_under, X_test_under, y_test_under))
# RFmodel.append(('RF OVERSAMPLE', RandomForestClassifier(),X_train_over, y_train_over, X_test_over, y_test_over))
RFmodel.append(('RF SMOTE', RandomForestClassifier(),X_train_smote, y_train_smote, X_test_smote, y_test_smote))
RFmodel.append(('RF ADASYN', RandomForestClassifier(),X_train_adasyn, y_train_adasyn, X_test_adasyn, y_test_adasyn))

performance(RFmodel)

"""Decision Tree Classifier"""

from sklearn.tree import DecisionTreeClassifier

DTmodel = []

DTmodel.append(('DT IMBALANCED', DecisionTreeClassifier(),X_train,y_train,X_test,y_test))
DTmodel.append(('DT UNDERSAMPLE', DecisionTreeClassifier(),X_train_under, y_train_under, X_test_under, y_test_under))
#DTmodel.append(('DT OVERSAMPLE', DecisionTreeClassifier(),X_train_over, y_train_over, X_test_over, y_test_over))
DTmodel.append(('DT SMOTE', DecisionTreeClassifier(),X_train_smote, y_train_smote, X_test_smote, y_test_smote))
DTmodel.append(('DT ADASYN', DecisionTreeClassifier() ,X_train_adasyn, y_train_adasyn, X_test_adasyn, y_test_adasyn))

performance(DTmodel)

comparision={
    'Model': names,
    'Accuracy': accuracy_tests,
    'AUC': aucs_tests,
    'Precision Score' : precision_tests,
    'Recall Score': recall_tests, 
    'F1 Score': f1_score_tests
}
print("Comparing performance of various Classifiers: \n \n")
comparision=pd.DataFrame(comparision)
comparision.sort_values('F1 Score',ascending=False)
