# -*- coding: utf-8 -*-
"""
Created on Fri May 31 17:18:15 2019

@author: mazaror
Similar to Modelling.py, but using 2 classes instead of three
"""
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import ElasticNet
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

tablon = pd.read_pickle('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/base_v1.pkl')
tablon = tablon[tablon['cant_jgos_h'] > 3]

tablon['dif_ptos_x_part'] = tablon['ptos_loc_tot']/tablon['cant_jgos_h'] - tablon['ptos_vis_tot']/tablon['cant_jgos_a']
tablon['dif_rend'] = tablon['ptos_loc_tot']/(tablon['cant_jgos_h']*3) - tablon['ptos_vis_tot']/(tablon['cant_jgos_a']*3)
tablon['dif_locloc_visvis'] = tablon['ptos_loc_loc'] - tablon['ptos_vis_vis']
tablon['dif_gol'] = tablon['dif_gol_loc'] - tablon['dif_gol_vis']
tablon['difgol_locloc_visvis'] = tablon['dif_gol_loc_loc'] - tablon['dif_gol_vis_vis']
tablon['dif_ptos_ls'] = tablon['ptos_h_last_season'] - tablon['ptos_a_last_season']
tablon['dif_bal_cant'] = tablon['balance_cant_h'] - tablon['balance_cant_a']
tablon['rat_bal'] = tablon['balance_h']/(tablon['balance_a'] + 1)
tablon['rat_inv_x_jug'] = tablon['gasto_x_jug_h']/(tablon['gasto_x_jug_a'] + 1)
tablon['rat_bal_2ls'] = tablon['balance_2ls_h']/(tablon['balance_2ls_a'] + 1)
tablon['rat_inv_2ls'] = tablon['inv_2ls_h']/(tablon['inv_2ls_a'] + 1)
tablon['dif_rend_ult5'] = tablon['rend_ult5_h'] - tablon['rend_ult5_a']
tablon['rat_inv'] = tablon['inv_ls_h']/(tablon['inv_ls_a'] + 1)
#tablon['rat_bal_ls'] = tablon['balance_ls_h']/(tablon['balance_ls_a'] + 1)


tablon = tablon[['Season','HomeTeam','AwayTeam','FTR','difgol_locloc_visvis',
                  'dif_rend','dif_locloc_visvis','dif_gol','dif_ptos_x_part',
                  'ult_res', 'gan_ult3_h','dif_rend_ult5',
                  'dif_ptos_ls','dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug',
                  'rat_inv_2ls','rat_inv','bal_cant_t30_tv','bal_mto_tv','pbb_loc',
                  'pbb_draw','pbb_vis']]

cols_elim = ['dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug','rat_inv']
tablon = tablon.drop(cols_elim, axis=1)
tablon = pd.get_dummies(tablon, columns=['FTR'])
tablon.isnull().any()

cols_bin_H = ['dif_ptos_x_part','dif_rend','dif_locloc_visvis','dif_gol',
'difgol_locloc_visvis','ult_res', 'gan_ult3_h','dif_rend_ult5',
'dif_ptos_ls','rat_inv_2ls','pbb_loc','pbb_draw','pbb_vis','FTR_H']

cols_bin_ = ['dif_ptos_x_part','dif_rend','dif_locloc_visvis','dif_gol',
'difgol_locloc_visvis','ult_res', 'gan_ult3_h','dif_rend_ult5',
'dif_ptos_ls','rat_inv_2ls','pbb_loc','pbb_draw','pbb_vis','FTR_H']


test = tablon[tablon['Season'] == 'T 18-19']
train = tablon[tablon['Season'] != 'T 18-19']

X_train = train[cols_bin_H].iloc[:,:13]
y_train = train[cols_bin_H].iloc[:,-1]

X_test = test[cols_bin_H].iloc[:,:13]
y_test = test[cols_bin_H].iloc[:,-1]

cols_scal= ['dif_locloc_visvis','dif_gol','difgol_locloc_visvis','dif_ptos_ls','rat_inv_2ls','pbb_loc','pbb_vis']
cols_minmax_scal=['pbb_loc','pbb_vis']

scaler = StandardScaler()
minmax = MinMaxScaler()

scaler.fit(tablon[cols_scal])
minmax.fit(tablon[cols_minmax_scal])

X_train[cols_scal] = scaler.transform(X_train[cols_scal])
X_train[cols_minmax_scal] = minmax.transform(X_train[cols_minmax_scal])

X_test[cols_scal] = scaler.transform(X_test[cols_scal])
X_test[cols_minmax_scal] = minmax.transform(X_test[cols_minmax_scal])

tablon.groupby(by='FTR_H').mean()

from sklearn.linear_model import LogisticRegression

lg = LogisticRegression()
lg.fit(X_train,y_train)

y_pred = lg.predict(X_test)
confusion_matrix(y_test,y_pred)
accuracy_score(y_test,y_pred)

probs = lg.predict_proba(X_test)
probs = pd.DataFrame(probs)
X_test['real'] = y_test.values 
X_test['pred'] = y_pred
X_test['pn_H'] = probs[0].values
X_test['pH'] = probs[1].values


X_test['acc'] = X_test.apply(lambda x: 1 if (x['real'] == x['pred'])&(x['real'] == 1) else 0, axis=1)


X_test['pH > 90'] = X_test.apply(lambda x: 1 if x['pH'] > 0.9 else 0, axis=1)
X_test['pH > 80'] = X_test.apply(lambda x: 1 if x['pH'] > 0.8 else 0, axis=1)
X_test['pH > 70'] = X_test.apply(lambda x: 1 if x['pH'] > 0.7 else 0, axis=1)
X_test['pH > 60'] = X_test.apply(lambda x: 1 if x['pH'] > 0.6 else 0, axis=1)

X_test['pH > 90'].value_counts()
X_test['pH > 80'].value_counts()
X_test['pH > 70'].value_counts()
X_test['pH > 60'].value_counts()

X_test[['pH > 90', 'acc']].groupby('pH > 90').mean()
X_test[['pH > 80', 'acc']].groupby('pH > 80').mean()
X_test[['pH > 70', 'acc']].groupby('pH > 70').mean()
X_test[['pH > 60', 'acc']].groupby('pH > 60').mean()

b365_1819 = pd.read_csv('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/b35418_19.csv', sep='\t')

X_test = X_test.reset_index()
X_test['b365_H'] = b365_1819['B365H'] 
X_test['b365_D'] = b365_1819['B365D'] 
X_test['b365_A'] = b365_1819['B365A'] 

X_test['bet365HDA'] = X_test.apply(lambda x: x['b365_H'] if x['pred'] == 1 else 0, axis= 1)

X_test['porc'] = X_test.apply(lambda x: (x['b365_H']*x['pH']-1+x['pH'])/x['b365_H'] if x['pred'] == 1 else 0 , axis= 1)
X_test['cto'] = X_test.apply(lambda x: x['porc']*1000, axis=1)
X_test['monto'] = X_test.apply(lambda x: x['b365_H']*x['acc']*x['porc']*1000, axis=1)

#Evaluación negocios total
X_test['monto'].sum() #Gano 71.2K inirtiendo 69.7
X_test['cto'].sum() 
X_test[X_test['pH > 60'] == 1]['monto'].sum() #Gano 31.5K invirtiedo 28.5K 
X_test[X_test['pH > 60'] == 1]['cto'].sum() 

X_test['cuota_H'] = 1/X_test['pH']



X_test['dif_cuota'] = X_test.apply(lambda x: x['cuota_H'] - x['b365_H'], axis= 1)

X_test.iloc[:5,10:].head()
X_test['cta_fav'] = X_test.apply(lambda x: 1 if x['dif_cuota'] > 0 else 0, axis=1)
X_test[X_test['cta_fav'] == 1]['monto'].sum() #Gano 45K si invierto 43.2K
X_test[X_test['cta_fav'] == 1]['cto'].sum() 
X_test['cta_fav'].value_counts() 



