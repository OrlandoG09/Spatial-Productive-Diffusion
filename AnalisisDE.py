
#Importar librerias 
#from math import e
#from operator import ge
import re
import pandas as pd
import geopandas as gpd
import libpysal.weights as lw
import openpyxl
import numpy as np

print("Librerias importadas")

#CARGA Y ALINEACION DE DATOS
#Cargar shapefile
geodf=gpd.read_file("mun22gw.shp")
geodf=geodf.set_index("CVEGEO")
geodf.index=geodf.index.astype(int)

#eliminar el nombre del indice 
geodf.index.name=None


#print(geodf.head(5))







#Cargar las 5 matrices 
#Cargar el archivo completo
archivoprincipal=pd.ExcelFile("Ms_1.xlsx")

#Crear un diccionario donde la clave es cada nombre de la hoja y el valor el df, ademas hacemos que la primer columnna sea el indice
hojasDicc=pd.read_excel(archivoprincipal,sheet_name=None,index_col=0)

#Creamos todos los df
df2003=hojasDicc["2003"]
df2008=hojasDicc["2008"]
df2013=hojasDicc["2013"]
df2018=hojasDicc["2018"]
df2023=hojasDicc["2023"]


#Borramos el nombre del indice
df2003.index.name = None
df2008.index.name = None
df2013.index.name = None
df2018.index.name = None
df2023.index.name = None

print("Df creados")



#Crear dataframes con los mismos indices
dffinal=pd.concat([df2003,df2008,df2013,df2018,df2023,geodf],axis=1,join="inner")


def indicesfaltantes(df1,df2):
 return df1.index.difference(df2.index).tolist()


Fa2003=indicesfaltantes(df2003,dffinal)
Fa2008=indicesfaltantes(df2008,dffinal)
Fa2013=indicesfaltantes(df2013,dffinal)
Fa2018=indicesfaltantes(df2018,dffinal)
Fa2023=indicesfaltantes(df2023,dffinal)
Fageodf=indicesfaltantes(geodf,dffinal)

df2003.drop(Fa2003,inplace=True)
df2008.drop(Fa2008,inplace=True)
df2013.drop(Fa2013,inplace=True)    
df2018.drop(Fa2018,inplace=True)
df2023.drop(Fa2023,inplace=True)
geodf.drop(Fageodf,inplace=True)

"""""
df2003.to_excel("df2003_ci.xlsx")
print("Indices faltantes eliminados respecto al df final")
df2008.to_excel("df2008_ci.xlsx")
"""


#DEFINIR LA ADYASCENCIA
#Crear la matriz de pesos
W = lw.Queen.from_dataframe(geodf,ids=geodf.index)

#print(W.neighbors[1001])

#Calcular el numero de municipios con esa rama al inicio del 2003 y al inicio de 2008

total_mun2003= df2003[3118].sum()
print(f"Total municipios con rama 3118 en 2003 {total_mun2003}")

total_mun2008=df2008[3118].sum()
print(f"Total municipios con rama 3118 en 2008 {total_mun2008}")



#Identificar adopciones y el rezagado espacial

#Matriz de adopciones (Devuelve un df con True en las adopciones y False en las no adopciones del mismo tamaño que los df originales)

adopciones1= (df2003==0) & (df2008==1)
adopciones2= (df2008==0) & (df2013==1)
adopciones3= (df2013==0) & (df2018==1)
adopciones4= (df2018==0) & (df2023==1)

#periodo completo
adopciones5= (df2003==0) & (df2023==1)

print("Matriz de adopciones creada")

#Lag espacial (Para indicar que numero de vecinos ya tenian esa rama al inicio del periodo)

lag1=lw.lag_spatial(W, df2003)
lag2=lw.lag_spatial(W, df2008)
lag3=lw.lag_spatial(W, df2013)
lag4=lw.lag_spatial(W, df2018)
print("Lag espacial calculado")

#Clasificar el contagio  

#Contagio inducido 
inducido1= (adopciones1==1) & (lag1>0)
inducido2= (adopciones2==1) & (lag2>0)
inducido3= (adopciones3==1) & (lag3>0)
inducido4= (adopciones4==1) & (lag4>0)

#periodo completo
inducido5= (adopciones5==1) & (lag1>0)
print("Contagio inducido calculado")

#Contagio espontaneo 
espontaneo1= (adopciones1==1) & (lag1==0)
espontaneo2= (adopciones2==1) & (lag2==0)
espontaneo3= (adopciones3==1) & (lag3==0)
espontaneo4= (adopciones4==1) & (lag4==0)

#periodo completo
espontaneo5= (adopciones5==1) & (lag1==0)

print("Contagio espontaneo calculado")

#Calcular las tasas de contagio inducido y espontaneo 

print("Calculando tasas a nivel RAMA (columna por columna)...")

# Calcular Numeradores por Rama (Total de municipios que adoptaron esa rama)
# axis=0 significa "suma hacia abajo (sumar todos los municipios para esa columna)"
total_inducido_rama1 = inducido1.sum(axis=0)
total_inducido_rama2 = inducido2.sum(axis=0)
total_inducido_rama3 = inducido3.sum(axis=0)
total_inducido_rama4 = inducido4.sum(axis=0)
#periodo completo
total_inducido_rama5_2 = inducido5.sum(axis=0) 

total_espontaneo_rama1 = espontaneo1.sum(axis=0)
total_espontaneo_rama2 = espontaneo2.sum(axis=0)
total_espontaneo_rama3 = espontaneo3.sum(axis=0)
total_espontaneo_rama4 = espontaneo4.sum(axis=0)
#periodo completo
total_espontaneo_rama5_2 = espontaneo5.sum(axis=0)    

#Calcular Denominadores por Rama (Total de municipios en riesgo para esa rama)
# Riesgo Inducido: Municipios que NO tenían esa rama Y sus vecinos SÍ
riesgo_ind_rama1 = ((df2003==0) & (lag1>0)).sum(axis=0)
riesgo_ind_rama2 = ((df2008==0) & (lag2>0)).sum(axis=0)
riesgo_ind_rama3 = ((df2013==0) & (lag3>0)).sum(axis=0)
riesgo_ind_rama4 = ((df2018==0) & (lag4>0)).sum(axis=0)
riesgo_ind_rama5_2 = ((df2003==0) & (lag1>0)).sum(axis=0) 
# Riesgo Espontáneo: Municipios que NO tenían esa rama Y sus vecinos TAMPOCO
riesgo_esp_rama1 = ((df2003==0) & (lag1==0)).sum(axis=0)
riesgo_esp_rama2 = ((df2008==0) & (lag2==0)).sum(axis=0)
riesgo_esp_rama3 = ((df2013==0) & (lag3==0)).sum(axis=0)
riesgo_esp_rama4 = ((df2018==0) & (lag4==0)).sum(axis=0)
riesgo_esp_rama5_2 = ((df2003==0) & (lag1==0)).sum(axis=0) 

#Calcular Tasas Finales por Rama
tasa_ind_rama1 = (total_inducido_rama1 / riesgo_ind_rama1).fillna(0)
tasa_ind_rama2 = (total_inducido_rama2 / riesgo_ind_rama2).fillna(0)
tasa_ind_rama3 = (total_inducido_rama3 / riesgo_ind_rama3).fillna(0)
tasa_ind_rama4 = (total_inducido_rama4 / riesgo_ind_rama4).fillna(0)

  

tasa_esp_rama1 = (total_espontaneo_rama1 / riesgo_esp_rama1).fillna(0)
tasa_esp_rama2 = (total_espontaneo_rama2 / riesgo_esp_rama2).fillna(0)
tasa_esp_rama3 = (total_espontaneo_rama3 / riesgo_esp_rama3).fillna(0)
tasa_esp_rama4 = (total_espontaneo_rama4 / riesgo_esp_rama4).fillna(0)



#Calculo de tasas acumuladas 2003-2023
total_inducido_rama5_1 = total_inducido_rama1 + total_inducido_rama2 + total_inducido_rama3 + total_inducido_rama4
total_espontaneo_rama5_1 = total_espontaneo_rama1 + total_espontaneo_rama2 + total_espontaneo_rama3 + total_espontaneo_rama4
riesgo_ind_rama5_1 = riesgo_ind_rama1 + riesgo_ind_rama2 + riesgo_ind_rama3 + riesgo_ind_rama4
riesgo_esp_rama5_1 = riesgo_esp_rama1 + riesgo_esp_rama2 + riesgo_esp_rama3 + riesgo_esp_rama4
tasa_ind_rama5_1 = (total_inducido_rama5_1 / riesgo_ind_rama5_1).fillna(0)
tasa_esp_rama5_1 = (total_espontaneo_rama5_1 / riesgo_esp_rama5_1).fillna(0)  

#Calculo de tasas acumuladas 2003-2023 (segundo metodo)
tasa_ind_rama5_2 = (total_inducido_rama5_2 / riesgo_ind_rama5_2).fillna(0)
tasa_esp_rama5_2 = (total_espontaneo_rama5_2 / riesgo_esp_rama5_2).fillna(0)  


#Guardar todo en un DataFrame
# USAMOS df2003.columns para que el índice sean las 86 RAMAS
resultados_ramas = pd.DataFrame(index=df2003.columns)

resultados_ramas['Tasa_Inducida_03_08'] = tasa_ind_rama1
resultados_ramas['Tasa_Inducida_08_13'] = tasa_ind_rama2
resultados_ramas['Tasa_Inducida_13_18'] = tasa_ind_rama3
resultados_ramas['Tasa_Inducida_18_23'] = tasa_ind_rama4
resultados_ramas['Tasa_Inducida_03_23(1)'] = tasa_ind_rama5_1
resultados_ramas['Tasa_Inducida_03_23(2)'] = tasa_ind_rama5_2

resultados_ramas['Tasa_Espontanea_03_08'] = tasa_esp_rama1
resultados_ramas['Tasa_Espontanea_08_13'] = tasa_esp_rama2
resultados_ramas['Tasa_Espontanea_13_18'] = tasa_esp_rama3
resultados_ramas['Tasa_Espontanea_18_23'] = tasa_esp_rama4
resultados_ramas['Tasa_Espontanea_03_23(1)'] = tasa_esp_rama5_1
resultados_ramas['Tasa_Espontanea_03_23(2)'] = tasa_esp_rama5_2

print("Cálculos por RAMA terminados.")
print(resultados_ramas.head())



# Guardar a Excel
resultados_ramas.to_excel("Tasas_Difusion_Por_Rama.xlsx")
print("Archivo 'Tasas_Difusion_Por_Rama.xlsx' guardado exitosamente.")

""""
#Calcular el numero de municipios contagiados y cuantos podian contagiar 
#de las ramas 3118, 3323, 3371 para el periodo 2003-2008

#RAMA 3118

adopciones_3118=adopciones1[3118]
lag_3118=lw.lag_spatial(W, df2003[3118])
inducido_3118= (adopciones_3118==1) & (lag_3118>0)
espontaneo_3118= (adopciones_3118==1) & (lag_3118==0)

#Total de municipios contagiados
total_inducido_3118 = inducido_3118.sum()
total_espontaneo_3118 = espontaneo_3118.sum()   

#Total de municipios que podian contagiarse
riesgo_ind_3118 = ((df2003[3118]==0) & (lag_3118>0)).sum()
riesgo_esp_3118 = ((df2003[3118]==0) & (lag_3118==0)).sum() 

print("Rama 3118 - 2003-2008")


#RAMA 3323
adopciones_3323=adopciones1[3323]
lag_3323=lw.lag_spatial(W, df2003[3323])
inducido_3323= (adopciones_3323==1) & (lag_3323>0)
espontaneo_3323= (adopciones_3323==1) & (lag_3323==0)

#Total de municipios contagiados
total_inducido_3323 = inducido_3323.sum()
total_espontaneo_3323 = espontaneo_3323.sum()   

#Total de municipios que podian contagiarse
riesgo_ind_3323 = ((df2003[3323]==0) & (lag_3323>0)).sum()
riesgo_esp_3323 = ((df2003[3323]==0) & (lag_3323==0)).sum() 

print("Rama 3323 - 2003-2008")

#RAMA 3371
adopciones_3371=adopciones1[3371]
lag_3371=lw.lag_spatial(W, df2003[3371])  
inducido_3371= (adopciones_3371==1) & (lag_3371>0)
espontaneo_3371= (adopciones_3371==1) & (lag_3371==0)   

#Total de municipios contagiados
total_inducido_3371 = inducido_3371.sum()   
total_espontaneo_3371 = espontaneo_3371.sum()   
#Total de municipios que podian contagiarse
riesgo_ind_3371 = ((df2003[3371]==0) & (lag_3371>0)).sum()
riesgo_esp_3371 = ((df2003[3371]==0) & (lag_3371==0)).sum()       

print("Rama 3371 - 2003-2008")  

#Crear el dataframe de resultados
ramas_interes = pd.DataFrame(index=[3118,3323,3371])

ramas_interes['Total_Inducido_03_08'] = [total_inducido_3118, total_inducido_3323, total_inducido_3371]
ramas_interes['Riesgo_Inducido_03_08'] = [riesgo_ind_3118, riesgo_ind_3323, riesgo_ind_3371]
ramas_interes["Total_espontaneo_03_08"]=[total_espontaneo_3118,total_espontaneo_3323,total_espontaneo_3371]
ramas_interes["Riesgo_espontaneo_03_08"]=[riesgo_esp_3118,riesgo_esp_3323,riesgo_esp_3371]



# Contar cuántos municipios PERDIERON la industria (Tenían en 2003 y NO en 2008)
extinciones_3118 = ((df2003[3118] == 1) & (df2008[3118] == 0)).sum()

# Comprobación matemática
neto_calculado = (total_inducido_3118 + total_espontaneo_3118) - extinciones_3118

extinciones_3323 = ((df2003[3323] == 1) & (df2008[3323] == 0)).sum()
neto_calculado_3323 = (total_inducido_3323 + total_espontaneo_3323) - extinciones_3323  

extinciones_3371 = ((df2003[3371] == 1) & (df2008[3371] == 0)).sum()
neto_calculado_3371 = (total_inducido_3371 + total_espontaneo_3371) - extinciones_3371  

ramas_interes['Extinciones_03_08'] = [extinciones_3118, extinciones_3323, extinciones_3371]
ramas_interes['Neto_Calculado_03_08'] = [neto_calculado, neto_calculado_3323, neto_calculado_3371]      

ramas_interes.to_excel("ramas_interes.xlsx")

"""
