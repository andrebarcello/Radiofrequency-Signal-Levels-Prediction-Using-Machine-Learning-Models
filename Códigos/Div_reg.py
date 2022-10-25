"""
Created on Sat Jun 29 23:19:49 2019

@author: Andre
"""
import pandas  as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import folium
import math
import numpy as np

#csv=pd.read_csv('File_1.csv', sep=',', encoding='ASCII')#Anapolis
#csv=pd.read_csv('File_2.csv', sep=';', encoding='ASCII')#Sidrolandia
csv=pd.read_csv('File_3.csv', sep=';', encoding='ASCII')#Camaqua


# Separa os dados de um determinado PCI
#csv=csv.loc[csv['PCI']==415]
csv=csv.loc[csv['PCI']==320]

#eliminando dados não utilizados
#csv = csv.drop(columns=["SessionID","TestID","StartTime","Band","MCC","MNC","ECI","eNBID","CellID","TAC","Channel","BW","PLMNId","pschrp"])
csv = csv.drop(columns=["StartTime","Band","MCC","MNC","ECI","eNBID","CellID","TAC","Channel","BW","PCI","PLMNId","pschrp"])#Camaqua

#calcula as medias dos valores medidos no mesmo ponto
csv = csv.groupby(['Lat', 'Lon'])['RSRP'].mean() .reset_index()

cor= ['orange', 'darkred', 'cadetblue', 'red', 'pink', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen', 'orange', 'darkred', 'cadetblue', 'red', 'white', 'darkpurple', 'blue', 'gray', 'green', 'purple', 'lightgrayblack', 'beige', 'lightgreen', 'lightred', 'darkblue', 'lightblue', 'pink', 'darkgreen']
cor1=cor;
razao=1;

print(csv.describe())

#Dividindo as regiões.....
def area_contem_cliente( a, c ):
    ponto = Point(c)
    poligono = Polygon(a)
    return poligono.contains(ponto)

#anapolis
#ponto_super_esquerda=[-16.280377, -48.995050]
#ponto_super_direita=[-16.280377, -48.917538]
#ponto_inferior_direita=[-16.349065, -48.917538]
#ponto_inferior_esquerda=[-16.349065, -48.995050]

#Sidrolandia
#ponto_super_esquerda=[-20.910330, -54.980760]
#ponto_super_direita=[-20.910330, -54.947660]
#ponto_inferior_direita=[-20.955930, -54.947660]
#ponto_inferior_esquerda=[-20.955930, -54.980760]

#Camaqua
ponto_super_esquerda=[-30.843300, -51.826600]
ponto_super_direita=[-30.843300, -51.780200]
ponto_inferior_direita=[-30.875900, -51.780200]
ponto_inferior_esquerda=[-30.875900, -51.826600]

regiao=[(ponto_super_direita),
        (ponto_super_esquerda),
        (ponto_inferior_esquerda),
        (ponto_inferior_direita)]


for i in range(csv.shape[0]):

     a=area_contem_cliente(regiao,(csv['Lat'][i], csv['Lon'][i]))
     if a == False:
         csv=csv.drop([i]);

#para 400 regioes colocar 20, para 900 regioes colocar 30
n=30;
print(csv.describe())

maximo=[max([regiao[0][0],regiao[1][0],regiao[2][0],regiao[3][0]]),
        max([regiao[0][1],regiao[1][1],regiao[2][1],regiao[3][1]])]
minimo=[min([regiao[0][0],regiao[1][0],regiao[2][0],regiao[3][0]]),
        min([regiao[0][1],regiao[1][1],regiao[2][1],regiao[3][1]])];
medio=[((maximo[0]+minimo[0])/2),((maximo[1]+minimo[1])/2)];


N=n*n;#numero de areas de decisão

lat=np.arange(minimo[0],maximo[0]+.0001,(maximo[0]-minimo[0])/(n));
lon=np.arange(minimo[1],maximo[1]+.0003,(maximo[1]-minimo[1])/(n));

area = [ [ [] for j in range(4) ] for i in range(n*n) ]

for i in range(n):
    for j in range(n):
        area[j+i*n]=[(lat[i],lon[j]),(lat[i],lon[j+1]),
            (lat[i+1],lon[j+1]),(lat[i+1],lon[j])]



#Classificando as amostras por região
for j in range(N):
    a=[]
    csv['regiao'+str(j)]='sim';

    for i in range(csv.shape[0]):

        a.append(area_contem_cliente(area[j],(csv.iloc[i]['Lat'], csv.iloc[i]['Lon'])))
    print("Região",j, "Criada") 

    csv['regiao'+str(j)]=a;

    a=[N+1]*csv.shape[0];

#Coluna Regiao que vai ser a classe e diz o numero da região daquela amostra
for k in range(N):
    for l in range(csv.shape[0]):
        if (csv.iloc[l]['regiao'+str(k)] == True):
            a[l]=k;

csv['regiao']=a;
csv1=csv.sort_values('regiao');



cor=[];lon=[];lat=[];rsrp=[];pci=[];regiao=[];

for i in range(int(csv1.shape[0]/razao)):
   if (csv1.iloc[i*razao]['regiao'] != (N+1)):
        regiao.append(csv1.iloc[i*razao]['regiao']);
        lon.append(csv1.iloc[i*razao]['Lon']);
        lat.append(csv1.iloc[i*razao]['Lat']);
        rsrp.append(csv1.iloc[i*razao]['RSRP']);
        print("Ponto",i,"de", (int(csv1.shape[0])), "Ok")

#Criando o DataFrame....
data = {
'time': time,
'RSRP': rsrp,
'Regiao': regiao,
'Lat': lat,
'Lon': lon
}

df = pd.DataFrame(data, columns=['RSRP','Regiao','Lat','Lon'])


# Salvando
df.to_csv('Selecionados.csv')
print("Fim")

razao=10;
#Gerando os pontos no Mapa........
ponto = csv.iloc[int(df.shape[0]/2)]
brasil = folium.Map(location=medio, zoom_start=15)

for i in range(int(df.shape[0]/razao)):
    if (df.iloc[i*razao]['Regiao'] != ((N+1))):
        cor_atual=df['Cor'][i*razao];
        ponto = df.iloc[i*razao];
        folium.Marker(
                      location=[ponto['Lat'], ponto['Lon']],
                      popup=df.iloc[i*razao]['Regiao'],
                      icon=folium.Icon(color=cor_atual)
        ).add_to(brasil)

