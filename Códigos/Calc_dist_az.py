# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:35:53 2021

@author: Andre
"""

import pandas as pd
import numpy as np
import geopy.distance
import math

#rotina para calculo do angulo da antena de trasmissão.
def get_bearing(lat2,lon2):
    dLon = lon2 - (-51.794696);
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(-30.847095)*math.sin(lat2) - math.sin(-30.847095)*math.cos(lat2)*math.cos(dLon);
    brng = np.rad2deg(math.atan2(y, x));
    if brng < 0: brng+= 360
    brng=round(brng)
    return brng

#rotina para calculo do ganho da antena
def get_gain(angle):
    a=angle+az;
    if a > 359: a = a - 360
    G=dant.iloc[a, 1]
    return G

    # Lê arquivo
df = pd.read_csv('Sel_Cama_PCI320_(900).csv', delimiter=',')
df = df[['Lon', 'Lat','RSRP','Regiao']]   
#df = pd.read_csv('MComp_HTZ_Cama.csv', delimiter=',')
dant = pd.read_csv('Antena_cama.csv', delimiter=';')

#coordenadas do transmissor
p1 = (-30.847095, -51.794696)#Camaqua
az = 120 #camaqua

#calcula as distâncias e angulos
dist=[]
bearing=[]
att=[]
Gant=[]
for _, pontos in df.iterrows():
    p2=[pontos['Lat'], pontos['Lon']]
    dist.append((geopy.distance.distance(p1, p2).km)*1000)
    bearing.append(get_bearing(pontos['Lat'], pontos['Lon']))

df["distancia"] = dist
df["bearing"] = bearing

for i in range(len(df)):
  ang=df.iloc[i,5]
  Gant.append(get_gain(ang))
 
df["Ganho"] = Gant

df=df.sort_values(by=['distancia'])

df.to_csv('Sel_Cama_PCI320_(900)_dis.csv')

print("End")
