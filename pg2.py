# -*- coding: utf-8 -*-
"""pg2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NHqCAFiBkEjWFX5fAGSURzbgBNat59KQ
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.model_selection import train_test_split,cross_validate, GridSearchCV

from sklearn.linear_model import LinearRegression,Lasso,Ridge,BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor



import warnings
warnings.filterwarnings("ignore")


from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn import linear_model
from sklearn.neighbors import (NeighborhoodComponentsAnalysis, KNeighborsClassifier)
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

df_train = pd.read_csv('/content/train.csv', index_col='id')
df_test = pd.read_csv('/content/test.csv', index_col='id')
sample_submission = pd.read_csv('/content/sample_submission.csv')

df = pd.concat([df_train,df_test], axis=0)

df

df.info()

(df.isna().sum()/len(df))*100

num_feat = list(df.select_dtypes(include = [int,float]).columns)
num_feat = num_feat[0:21]

for col in num_feat:
    df[col].fillna(df[col].mean(),inplace = True)

(df.isna().sum()/len(df))*100

print(df['attribute_0'].unique())
print(df['attribute_1'].unique())

df['attribute_0'][df['failure']==1].value_counts()

df['attribute_0'][df['failure']==0].value_counts()

print(16723/(16723+4597))
print(4198/(4198+1052))

"""Принципиальной разницы практически нет, поэтому просто закодируем material_7 как 7, material_5 как 5"""

df['attribute_0'] = df['attribute_0'].apply(lambda x: 7 if x =='material_7' else 5)

df['attribute_1'].unique()

df['attribute_1'] = df['attribute_1'].apply(lambda x: rep_func(x))

def rep_func(x):
    if x == 'material_7':
        x=7
        return x
    elif x =='material_5':
        x=5
        return x
    elif x=='material_6':
        x=6
        return x
    else:
        x=8
        return x

df['attribute_1'].unique()

# в атрибуте 0  5 и 8  одинаковы, но 6 сильно лучше

# ранжируем атрибут 1, по убыванию: 6,8,5,7
def at_1_range(x):
    if x == 6:
      x=2
      return x
    else:
      x=1.5
      return x

df['attribute_1'] = df['attribute_1'].apply(lambda x: at_1_range(x))

df_train['attribute_2'][df_train['failure']==0].value_counts()/df_train['attribute_2'].value_counts()

# в атрибуте 2 никакой разницы нет, но все равно стандартизируем
def at_2_range(x):
    if x == 6:
        x=1.5
        return x
    elif x ==8:
        x=1.7
        return x
    elif x==6:
        x=1.6
        return x
    else:
        x=1.4
        return x

df['attribute_2'] = df['attribute_2'].apply(lambda x: at_2_range(x))

df_train['attribute_3'][df_train['failure']==0].value_counts()/df_train['attribute_3'].value_counts()

def at_3_range(x):
    if x == 9:
        x=1.7
        return x
    elif x ==8:
        x=1.7
        return x
    elif x==6:
        x=1.6
        return x
    else:
        x=1.5
        return x

df['attribute_3'] = df['attribute_3'].apply(lambda x: at_3_range(x))

# ранжировали атрибуты, пробуем запустить в модель, пустые данные так же заменены нулями
df3_train = df[df["failure"].notna()]
df3_test = df[df["failure"].isna()]

print(df3_train.shape)
print(df3_test.shape)

X = df3_train.drop(['failure','product_code'], axis=1)
y = df3_train['failure']

X_train, X_test, y_train, y_test = train_test_split(X, y)

pipe = Pipeline([('classifier', LogisticRegression())])


param_grid = [
    {'classifier' : [LogisticRegression()]
    },
    {'classifier' : [RandomForestClassifier()]
    },
    {'classifier' : [linear_model.LassoLars()]
    },
    {'classifier' : [KNeighborsClassifier()]
    },
    {'classifier' : [GaussianNB()]
    },
    {'classifier' : [GradientBoostingClassifier()]
    }
]



clf = GridSearchCV(pipe, param_grid = param_grid, cv = 5, verbose=True, n_jobs=-1, scoring='roc_auc')



best_clf = clf.fit(X_train, y_train)

best_clf.best_estimator_

best_clf.best_score_

lr = LogisticRegression()

lr.fit(X_train, y_train)

y_predict = lr.predict(X_test)
  

print("ROC-AUC %.3f" %metrics.roc_auc_score(y_test, y_predict))

sub_redict = lr.predict_proba(df3_test.drop(['failure','product_code'], axis=1))[:, 1]


sample_submission['failure'] = sub_redict
sample_submission.to_csv('submission_lr1.csv', index = False)