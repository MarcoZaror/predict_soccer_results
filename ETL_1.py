# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:50:38 2019

@author: mazaror

First part of the ETL, importing and structuring the information
"""

import pandas as pd
import time
from scipy.stats import poisson 

start = time.time()

base = pd.read_csv('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/base_v1.csv', sep=';')
base['Date'] = pd.to_datetime(base['Date'], format="%d-%m-%Y") 

base['cant_jgos_h'] = base.apply(get_fecha_h,axis=1)
base['cant_jgos_a'] = base.apply(get_fecha_a,axis=1)

#Points of the home team playing in its field, in the other teams' field and total
base['ptos_loc_loc'] = base.apply(get_ptos_team_h_h, axis=1)
base['ptos_loc_vis'] = base.apply(get_ptos_team_h_a, axis=1)
base['ptos_loc_tot'] = base.apply(get_ptos_team_h, axis=1)

#Points of the away team playing in their field, in the other teams' field and total
base['ptos_vis_loc'] = base.apply(get_ptos_team_a_h, axis=1)
base['ptos_vis_vis'] = base.apply(get_ptos_team_a_a, axis=1)
base['ptos_vis_tot'] = base.apply(get_ptos_team_a, axis=1)

#Goals scored by the home team
base['goles_loc'] = base.apply(get_gol_fav_team_h, axis = 1)

#Goals scored by the away team
base['goles_vis'] = base.apply(get_gol_fav_team_a, axis = 1)

#Goals scored by the home team playing in their field, and in other teams' field
base['goles_loc_loc'] = base.apply(get_gol_fav_team_h_h, axis = 1)
base['goles_loc_vis'] = base.apply(get_gol_fav_team_h_a, axis = 1) 

#Goals scored by the away team playing in their field, and in other teams' field
base['goles_vis_loc'] = base.apply(get_gol_fav_team_a_h, axis = 1)
base['goles_vis_vis'] = base.apply(get_gol_fav_team_a_a, axis = 1)

#Goals received by the home team
base['goles_con_loc'] = base.apply(get_gol_con_team_h, axis = 1)

#Goals received by the away team
base['goles_con_vis'] = base.apply(get_gol_con_team_a, axis = 1)

#Goals received by the home team playing in their field, and in other teams' field
base['goles_con_loc_loc'] = base.apply(get_gol_con_team_h_h, axis = 1)
base['goles_con_loc_vis'] = base.apply(get_gol_con_team_h_a, axis = 1) 

#Goals received by the away team playing in their field, and in other teams' field
base['goles_con_vis_loc'] = base.apply(get_gol_con_team_a_h, axis = 1)
base['goles_con_vis_vis'] = base.apply(get_gol_con_team_a_a, axis = 1)

#Difference between scored and received goals for the home and away team
base['dif_gol_loc'] = base['goles_loc'] - base['goles_con_loc']
base['dif_gol_vis'] = base['goles_vis'] - base['goles_con_vis']

#Difference between scored and received goals for the home team, playing in ther field and in other teams' field
base['dif_gol_loc_loc'] = base['goles_loc_loc'] - base['goles_con_loc_loc']
base['dif_gol_loc_vis'] = base['goles_loc_vis'] - base['goles_con_loc_vis']

#Difference between scored and received goals for the away team, playing in ther field and in other teams' field
base['dif_gol_vis_loc'] = base['goles_vis_loc'] - base['goles_con_vis_loc']
base['dif_gol_vis_vis'] = base['goles_vis_vis'] - base['goles_con_vis_vis']

seasons = pd.DataFrame([['T 0-1',1],['T 1-2',2],['T 2-3',3],['T 3-4',4],['T 4-5',5],['T 5-6',6], 
                        ['T 6-7',7],['T 7-8',8], ['T 8-9',9], ['T 9-10',10], ['T 10-11',11],
                        ['T 11-12',12],['T 12-13',13],['T 13-14',14], ['T 14-15',15],
                        ['T 15-16',16], ['T 16-17',17],['T 17-18',18], ['T 18-19',19]])
seasons.columns = ['Season','season_num']

#Merging season information (not all seasons considered)
base = pd.merge(base, seasons, how ='left', on = ['Season','Season'])

#Last result
base['ult_res'] = base.apply(get_ult_res, axis=1)

#Points obtained by the home and away team
base['ptos_loc_tot_aux'] =  base.apply(get_ptos_team_h_aux, axis =1)
base['ptos_vis_tot_aux'] =  base.apply(get_ptos_team_a_aux, axis =1)

#Points obtained by the home and away team in the last season
base['ptos_h_last_season'] =  base.apply(get_ptos_last_season_h, axis =1)
base['ptos_a_last_season'] =  base.apply(get_ptos_last_season_a, axis =1)

# Incorporating data about incomes and outcomes by transferences
dict_teams = pd.read_csv('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/dic_teams.csv', sep='\t')
exp_inc = pd.read_csv('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/exp_inc.csv', sep='\t')

exp_inc = pd.merge(exp_inc, seasons, how ='left', on = ['Season'])

#Generating new variables with the latter information
exp_inc['gasto_x_jug'] = exp_inc['expenditures']/exp_inc['arrivals']
exp_inc['balance_cant'] = exp_inc['arrivals'] - exp_inc['departures']
exp_inc['gan_x_jug'] = exp_inc['incomes']/exp_inc['departures']
exp_inc['ratio_balance'] = exp_inc['expenditures']/exp_inc['incomes']
exp_inc['balance_resta_aux'] = exp_inc['expenditures'] - exp_inc['incomes']
exp_inc['balance_ls'] = exp_inc.apply(get_bal_ls, axis=1)
exp_inc['balance_2ls'] = exp_inc['balance_resta_aux'] + exp_inc['balance_ls']
exp_inc['inv_ls'] = exp_inc.apply(get_inv_ls, axis=1)
exp_inc['inv_2ls'] = exp_inc['inv_ls'] + exp_inc['expenditures']


exp_inc = pd.merge(exp_inc, dict_teams, how ='left', left_on = ['team'], right_on=['exp_inc'])


#Generating the full base and computing a couple of more variables
exp_inc2 = exp_inc[['Season','team','arrivals','balance','gasto_x_jug','balance_cant','gan_x_jug','res','ratio_balance','balance_2ls','inv_ls','inv_2ls']]
base2 = pd.merge(base, exp_inc2, how ='left', left_on = ['Season','HomeTeam'], right_on = ['Season','res'])

base2 = base2.rename(index = str,columns={'arrivals':'arrivals_h', 'balance':'balance_h',
                                          'gasto_x_jug':'gasto_x_jug_h',
                                          'balance_cant':'balance_cant_h',
                                          'gan_x_jug':'gan_x_jug_h',
                                          'ratio_balance':'ratio_balance_h',
                                          'balance_2ls': 'balance_2ls_h',
                                          'inv_ls':'inv_ls_h',
                                          'inv_2ls':'inv_2ls_h',
                                          'expenditures':'expenditures_h'
                                          })

base3 = pd.merge(base2, exp_inc2, how ='left', left_on = ['Season','AwayTeam'], right_on = ['Season','res'])

base3 = base3.rename(index = str,columns={'arrivals':'arrivals_a', 'balance':'balance_a',
                                          'gasto_x_jug':'gasto_x_jug_a',
                                          'balance_cant':'balance_cant_a',
                                          'gan_x_jug':'gan_x_jug_a',
                                          'ratio_balance':'ratio_balance_a',
                                          'balance_2ls': 'balance_2ls_a',
                                          'inv_ls':'inv_ls_a',
                                          'inv_2ls':'inv_2ls_a',
                                          'expenditures':'expenditures_a'
                                          })

#Average points obtained by game for home and away team
base3['ptos_x_part_h'] = base3['ptos_loc_tot']/base3['cant_jgos_h']
base3['ptos_x_part_a'] = base3['ptos_vis_tot']/base3['cant_jgos_a']

#Last 3 results between the teams
base3['gan_ult3_h'] = base3.apply(get_ult_3res_h, axis=1)
base3['gan_ult3_a'] = base3.apply(get_ult_3res_a, axis=1)

#Number of matches for home team playing in their field
base3['cant_part_h_h'] = base3.apply(get_fecha_h_h, axis=1)

#Number of matches for away team playing away
base3['cant_part_a_a'] = base3.apply(get_fecha_a_a, axis=1)

#Performance of the teams in the last 5 matches
base3['rend_ult5_h'] = base3.apply(rend_team_ult5_h, axis = 1)
base3['rend_ult5_a'] = base3.apply(rend_team_ult5_a, axis = 1)

base3 = base3.drop(['res_x','team_x','team_y','res_y'], axis= 1)

#base3.hist('balance_cant_a', by='FTR' ,bins= 20, figsize=(15,10))


#Average of goals per match by home team
gol_loc = base3[['Season','FTHG']].groupby(by= 'Season').sum()
gol_loc['gol_loc_x_part_t'] = gol_loc['FTHG']/380
gol_loc = gol_loc.reset_index()
gol_loc = gol_loc.drop('FTHG', axis=1)

#Average of goals per match by away team
gol_vis = base3[['Season','FTAG']].groupby(by= 'Season').sum()
gol_vis['gol_vis_x_part_t'] = gol_vis['FTAG']/380
gol_vis = gol_vis.reset_index()
gol_vis = gol_vis.drop('FTAG', axis=1)

base4 = pd.merge(base3, gol_loc, how ='left', on = ['Season'])
base5 = pd.merge(base4, gol_vis, how ='left', on = ['Season'])

base5['rat_ataq_loc'] = (base5['goles_loc_loc']/base5['cant_part_h_h'])/base5['gol_loc_x_part_t']
base5['rat_ataq_vis'] = (base5['goles_vis_vis']/base5['cant_part_a_a'])/base5['gol_vis_x_part_t']
base5['rat_golcon_loc'] =(base5['goles_con_loc_loc']/base5['cant_part_h_h'])/base5['gol_vis_x_part_t']
base5['rat_golcon_vis'] =(base5['goles_con_vis_vis']/base5['cant_part_a_a'])/base5['gol_loc_x_part_t']
base5.info()

base5['pron_gol_loc'] = base5['rat_ataq_loc']*base5['rat_golcon_vis']*base5['gol_loc_x_part_t']
base5['pron_gol_vis'] = base5['rat_ataq_vis']*base5['rat_golcon_loc']*base5['gol_vis_x_part_t']  

base5['pbb_loc'] = base5.apply(get_pbb_gol_loc, axis=1)
base5['pbb_draw'] = base5.apply(get_pbb_gol_draw, axis=1)
base5['pbb_vis'] = base5.apply(get_pbb_gol_vis, axis=1)


#Add new information about each team balance prior to the league
tr_cbos = pd.read_csv('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/transfer_cambios_py.csv', sep='\t')
tr_cbos = tr_cbos[['Temporada','Ranking','Position','Club 1','Club 2','Liga 1','Liga 2','Monto 3']]
vta = tr_cbos[tr_cbos['Liga 1'] == 'England Premier League']
inv = tr_cbos[tr_cbos['Liga 2'] == 'England Premier League']

dict_teams_inv = dict_teams[['transfer2','res']]
dict_teams_vta = dict_teams[['transfer1','res']]

vta2 = pd.merge(vta, dict_teams_vta, how='left', left_on='Club 1', right_on='transfer1')
inv2 = pd.merge(inv, dict_teams_inv, how='left', left_on='Club 2', right_on='transfer2')
vta2 = vta2[vta2['transfer1'].isnull() == False]
inv2 = inv2[inv2['transfer2'].isnull() == False]
vta2 = vta2[['Temporada','Ranking','res','Monto 3']]
inv2 = inv2[['Temporada','Ranking','res','Monto 3']]


#Last changes
base5['cant_jug_comp_t30_h'] = base5.apply(get_cant_jug_compr_top30_h, axis=1)
base5['cant_mto_inv_h'] = base5.apply(get_monto_inv_h, axis=1)
base5['cant_jug_vend_t30_h'] = base5.apply(get_cant_jug_vend_top30_h, axis=1)
base5['cant_mto_vend_h'] = base5.apply(get_monto_vend_h, axis=1)

base5['cant_jug_comp_t30_a'] = base5.apply(get_cant_jug_compr_top30_a, axis=1)
base5['cant_mto_inv_a'] = base5.apply(get_monto_inv_a, axis=1)
base5['cant_jug_vend_t30_a'] = base5.apply(get_cant_jug_vend_top30_a, axis=1)
base5['cant_mto_vend_a'] = base5.apply(get_monto_vend_a, axis=1)

base5['bal_cant_t30_tv'] = (base5['cant_jug_comp_t30_h'] - base5['cant_jug_vend_t30_h'])-(base5['cant_jug_comp_t30_a'] - base5['cant_jug_vend_t30_a'])
base5['bal_mto_tv'] = (base5['cant_mto_inv_h'] - base5['cant_mto_vend_h'])-(base5['cant_mto_inv_a'] - base5['cant_mto_vend_a'])

base5.to_pickle('C:/Users/mazaror/Documents/Respaldo Maro Zaror/Personal/Python/Proyectos/Futbol/base_v1.pkl')
del dict_teams, base, base2, base3,base4,seasons,exp_inc,exp_inc2, gol_loc, gol_vis, base5, dict_teams_inv, dict_teams_vta, inv,inv2,vta,vta2,tr_cbos

end =time.time()
tiempo = end - start
print('Tiempo utilizado: '+str(tiempo))
del end,start,tiempo

