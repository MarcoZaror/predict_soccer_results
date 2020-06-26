# -*- coding: utf-8 -*-
"""
Created on Mon May 27 10:08:26 2019

@author: mazaror
Second part of the ETL
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

import matplotlib.pyplot as plt

#Import base created in ETL_1
tablon = pd.read_pickle('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/base_v1.pkl')
tablon = tablon[tablon['cant_jgos_h'] > 3]
tablon.isnull().any()
tablon[tablon['XXX'].isnull() == True].iloc[:10,:]

#Add more advanced variables
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


#Select only the columns that show discriminative power
tablon = tablon[['Season','HomeTeam','AwayTeam','FTR',
                  'dif_ptos_x_part','dif_rend','dif_locloc_visvis','dif_gol',
                  'difgol_locloc_visvis','ult_res', 'gan_ult3_h','dif_rend_ult5',
                  'dif_ptos_ls','dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug',
                  'rat_inv_2ls','rat_inv','pbb_loc','pbb_draw','pbb_vis']]

columns= ['FTR','dif_ptos_x_part','dif_rend','dif_locloc_visvis','dif_gol',
          'difgol_locloc_visvis','ult_res', 'gan_ult3_h','dif_rend_ult5',
          'dif_ptos_ls','dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug',
          'rat_inv_2ls','rat_inv','pbb_loc','pbb_draw','pbb_vis']
tablon2 = tablon[columns]

# A couple of extra analysis of the database
tablon2.info()
tablon2.groupby(by='FTR').mean()
tablon2['FTR'].value_counts() #H 2.713 - A 1.627 - D 1.440
cols = ['FTR','dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug','rat_inv']
cols_elim = ['dif_bal_cant','rat_bal','rat_bal_2ls','rat_inv_x_jug','rat_inv']

tab_test = tablon[cols]
tab_test.boxplot('rat_bal', by= 'FTR')
tab_test.hist('rat_bal', by= 'FTR', bins=20)
tab_test.describe()
tab_test = tab_test.drop('std_dif_bal_cant',axis=1)
scaler = StandardScaler()
scaler.fit(tab_test['rat_inv_x_jug'].reshape(-1,1))
tab_test['std_rat_inv_x_jug'] = scaler.transform(tab_test['rat_inv_x_jug'].reshape(-1,1))

tab_test2 = tab_test[(tab_test['std_rat_inv_x_jug'] > -2) & (tab_test['std_rat_inv_x_jug'] < 2)]
tab_test.groupby('FTR').mean()


tablon = tablon.drop(cols_elim, axis=1)
 
tablon3.describe()
tablon3.groupby('FTR').mean()

tablon2.to_pickle('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/base_v2.pkl')