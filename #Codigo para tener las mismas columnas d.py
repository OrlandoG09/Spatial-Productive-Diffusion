#Codigo para tener las mismas columnas de 5 archivos diferentes y llevar registro de las columnas eliminadas 

import pandas as pd

archivoprincipal=pd.ExcelFile("Ms_1.xlsx")

hojasDicc=pd.read_excel(archivoprincipal,sheet_name=None,index_col=0)



df2003=hojasDicc["2003"]
df2008=hojasDicc["2008"]
df2013=hojasDicc["2013"]
df2018=hojasDicc["2018"]
df2023=hojasDicc["2023"]

df2003.index.name = None
df2008.index.name = None
df2013.index.name = None
df2018.index.name = None
df2023.index.name = None

print("Df creados")

dffinal=pd.concat([df2003,df2008,df2013,df2018,df2023],axis=1,join="inner")



def indicesfaltantes(df1,df2):
 return df1.index.difference(df2.index).tolist()


Fa2003=indicesfaltantes(df2003,dffinal)
Fa2008=indicesfaltantes(df2008,dffinal)
Fa2013=indicesfaltantes(df2013,dffinal)
Fa2018=indicesfaltantes(df2018,dffinal)
Fa2023=indicesfaltantes(df2023,dffinal)


print(Fa2003)
print("\n")
print(Fa2008)
print("\n")
print(Fa2013)
print("\n")
print(Fa2018)
print("\n")
print(Fa2023)


