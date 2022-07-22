# Nella prima parte di questo script divido la provincia di Trento in zone riferendole alla stazione meteo più vicina. Abbiamo considerato solo le zone in cui è presente almeno una linea. 
from trentodatalib import consumi, meteo, inquinamento 
from trentodatalib import funzioni as fz 

import sys, os
import pandas as pd
import numpy as np


# riprendendo il database elaborato nel file meteo consumi e lo sistemo al fine di ottenere dati meteo mediati o sommati sulle fasce orarie 
#######Domanda queste linee di codice forse è meglio metetrle direttamente in meteo ????
#creo due pd.Series che contengono dati raggruppati e mediati/sommati come voglio
'''meanTempGb  = meteo_df.groupby(['station', meteo_df['datetime'].dt.date,'TimeRange']  )['temperatures'].mean() 
sumPrecipGb = meteo_df.groupby(['station', meteo_df['datetime'].dt.date,'TimeRange']  )['precipitations'].sum() 
meanWindsGb = meteo_df.groupby(['station', meteo_df['datetime'].dt.date,'TimeRange']  )['windSpeed'].mean()

# unisco in un dataframe e lo aggiusto
dicttmp = { 'meanTemperature': meanTempGb, 'precipitations': sumPrecipGb, 'meanWinds': meanWindsGb}
df_tmp_gb = pd.DataFrame(dicttmp).reset_index()
df_tmp_gb.rename(columns={'datetime':'date'} , inplace=True) 

#voglio unirlo con i dati di geometry, e altri dati giornalieri non usati nel groupby
df_tmp_tomerge = meteo_df[['station', 'geometry','elevation', 'minTemperature', 'maxTemperature', 'datetime', 'isWeekend', 'TimeRange']]
#il seguente comando genera una warning ma a quanto pare è un falso positivo. 
#serve a tenere solo le date e a buttare le ore
df_tmp_tomerge['date'] =df_tmp_tomerge['datetime'].dt.date
#togliendo datetime ho un df con un sacco di righe uguali, le butto con .drop_duplicates()
df_tmp_tomerge.drop(columns='datetime', inplace=True)
df_tmp_tomerge  = df_tmp_tomerge.loc[df_tmp_tomerge.astype(str).drop_duplicates().index].reset_index()
df_tmp_tomerge.drop(columns='index', inplace=True)
#finalmente unisco i due dataframe
meteo_df = pd.merge(left=df_tmp_tomerge, right=df_tmp_gb, on=['station', 'date', 'TimeRange'])
'''

# Ora provo ad associare le celle di territorio 
'''
gdfLineCells = pd.merge(left=rawdata.gridraw, right=consumi.df_linee, left_on='id', right_on='SQUAREID', how='right').drop(columns='id')
gdfLineCells[['geometry', 'SQUAREID']].drop_duplicates().reset_index().drop(columns='index')
#per calcolare il criordiniamoentroide è tecnicamente opportuno trasformare coordinate sferiche in km
#anche se non dovrebbe fare molta differenza
gdfLineCells.to_crs(epsg=3035, inplace=True)
gdfLineCells['centroid'] = gdfLineCells['geometry'].centroid
mapsta.df_mappa_stazioni.to_crs(epsg=3035, inplace=True)

'''
#per evitare conflitti uso .copy()
gdfLineCells = meteo.gdfLineCells.copy()
meteo_df = meteo.meteo_df.copy()
df_consumi = consumi.df_consumi.copy()
df_linee = consumi.df_linee
dfInqTrento = inquinamento.dfInqTrento

### creo un dataframe con SQUAREID e codici stazioni:
#gdfLineCells contiene associazioni delle celle alla stazione meteo più vicina 
df_suddivisione = gdfLineCells[['SQUAREID', 'nearestStation']].drop_duplicates().reset_index().drop(columns='index')
# unisco dati dei consumi sulle celle con quelli della suddivisione in zone
# in modo da suddividere i consumi in zone
df_consumi = pd.merge(left=df_consumi, right=df_suddivisione, on='SQUAREID', how='left')
# sommo i consumi di ogni zona
df_consumi = df_consumi.groupby(['nearestStation', 'datetime', 'TimeRange', 'isWeekend'])['consumo_della_cella'].sum().reset_index()
#rinomino un po' di colonne per comodità nell'uso di merge
df_consumi.rename(columns={'nearestStation':'station', 'datetime':'date', 'consumo_della_cella':'consumoTerritorio'} , inplace=True)
#segno la durata di ogni fascia oraria così da poter normalizzare il consumo
durataFasce = {'day':11, 'evening':5, 'night':8}
#ad ogni time range associo la sua durata in ore con .map
df_consumi['N_ORE'] = df_consumi['TimeRange'].map(durataFasce)
#finalmente merge tra dati di consumi e meteo
df_meteo_consumi = pd.merge(left=df_consumi, right=meteo_df, on=['station', 'date', 'TimeRange', 'isWeekend'])
#conto le ubicazioni in ogni squareid
df_ubi_squareid = df_linee.groupby('SQUAREID')['NR_UBICAZIONI'].sum().reset_index()
#e unisco il df appena ottenuto con quello contenente SQUAREID e codicistazione
df_ubi_territori = pd.merge(left=df_ubi_squareid, right=df_suddivisione, on='SQUAREID')
#così posso sommare le ubicazioni su ogni territorio
df_ubi_territori = df_ubi_territori.groupby('nearestStation')['NR_UBICAZIONI'].sum().reset_index()
df_ubi_territori.rename(columns={'nearestStation':'station'}, inplace=True) 
#unisco le ubicazioniperterritorio al df con tutti i dati
df_meteo_consumi = pd.merge(left=df_meteo_consumi, right=df_ubi_territori, how='left', on='station')
#in ultimo, aggiungo una colonna per indicare quanto è il consumo/(ora*ubicazione) in quel territorio
df_meteo_consumi['consumoOrarioUbicazione'] = df_meteo_consumi['consumoTerritorio']/(df_meteo_consumi['NR_UBICAZIONI']*df_meteo_consumi['N_ORE'])
#la stazione meteo di trento è T0129 , vedi mappa sopra
dfTrento = df_meteo_consumi[ (df_meteo_consumi['station']=='T0129')
                            & (df_meteo_consumi['isWeekend']==False)  ]                     
dfTrentoZone = df_meteo_consumi[  ((df_meteo_consumi['station']=='T0129') | (df_meteo_consumi['station']=='T0135'))
                            & (df_meteo_consumi['isWeekend']==False)  ]       

# finalmente unisco con dati di meteo e consumi di Trento


dfTrentoZoneDay = dfTrentoZone[ dfTrentoZone['TimeRange'] == 'day' ]
dfTrentoZoneEv = dfTrentoZone[ dfTrentoZone['TimeRange'] == 'evening' ]
dfTrentoZoneNight = dfTrentoZone[ dfTrentoZone['TimeRange'] == 'night' ]

dfTrentoZoneDay = fz.categorizza_consumi(dfTrentoZoneDay, 'consumoOrarioUbicazione')
dfTrentoZoneEv = fz.categorizza_consumi(dfTrentoZoneEv, 'consumoOrarioUbicazione')
dfTrentoZoneNight = fz.categorizza_consumi(dfTrentoZoneNight, 'consumoOrarioUbicazione')

#dopo aver affiancato il giorno x e il giorno x+1 in ogni df, si vuole eliminare queste colonne dai df
columns_to_drop2 = ['date_x+1' , 'TimeRange_x', 'isWeekend_x','dayOfWeek_x',
                      'TimeRange_x+1', 'isWeekend_x+1', 'dayOfWeek_x+1']

# dfTrentoZoneDay['dayOfWeek'] = dfTrentoZoneDay['date'].apply(datetime.weekday)
# print(dfTrentoZoneDay['dayOfWeek'])

#dati relativi alla zona A del territorio di Trento
dfTrentoZoneDayA = fz.addNextDay(dfTrentoZoneDay[ dfTrentoZoneDay['station'] == 'T0129'  ].reset_index().drop(columns='index') , columns_to_drop2)
dfTrentoZoneEvA = fz.addNextDay(dfTrentoZoneEv[ dfTrentoZoneEv['station'] == 'T0129'  ].reset_index().drop(columns='index') , columns_to_drop2)
dfTrentoZoneNightA =  fz.addNextDay(dfTrentoZoneNight[ dfTrentoZoneNight['station'] == 'T0129'  ].reset_index().drop(columns='index') , columns_to_drop2)

#dati relativi alla zona B del territorio di Trento
dfTrentoZoneDayB = fz.addNextDay(dfTrentoZoneDay[ dfTrentoZoneDay['station'] == 'T0135'  ].reset_index().drop(columns='index') , columns_to_drop2)
dfTrentoZoneEvB = fz.addNextDay(dfTrentoZoneEv[ dfTrentoZoneEv['station'] == 'T0135'  ].reset_index().drop(columns='index') , columns_to_drop2)
dfTrentoZoneNightB =  fz.addNextDay(dfTrentoZoneNight[ dfTrentoZoneNight['station'] == 'T0135'  ].reset_index().drop(columns='index') , columns_to_drop2)

#unisco tutto
dfTrentoZoneDay = pd.concat([dfTrentoZoneDayA, dfTrentoZoneDayB]).reset_index(drop=True)
dfTrentoZoneEv = pd.concat([dfTrentoZoneEvA, dfTrentoZoneEvB]).reset_index(drop=True)
dfTrentoZoneNight = pd.concat([dfTrentoZoneNightA, dfTrentoZoneNightB]).reset_index(drop=True)

#salvo in file esterni usando pickle
dfTrentoZoneDay.to_pickle(os.path.join(os.path.dirname(__file__),"../data/processed/datiTrentoDay.pkl"))
dfTrentoZoneEv.to_pickle(os.path.join(os.path.dirname(__file__),"../data/processed/datiTrentoEv.pkl"))
dfTrentoZoneNight.to_pickle(os.path.join(os.path.dirname(__file__),"../data/processed/datiTrentoNight.pkl"))


print(dfTrentoZoneDay.head())

