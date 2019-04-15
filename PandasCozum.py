# from os import listdir
# from os.path import isfile,join
# yol = r"E:\Projelerim\single_machine_scheduling\DENEME CSV SETLER\DENEME CSV SETLER\I=5, J=10"
# dosya = [f for f in listdir(yol) if isfile(join(yol,f))]

# print(dosya)
# input()

import pandas as pd
import numpy as np
sutun = ["Job","O1","O2","O3","O4","O5","PROC","SETUP"]
data =  pd.read_csv(r"E:\Projelerim\single_machine_scheduling\DENEME CSV SETLER\DENEME CSV SETLER\I=5, J=10\Experiment35.csv",delimiter=";")
sutun.append("SUM")
df = pd.DataFrame(columns=sutun)
df.Job = data.Job
df.SETUP = data.SETUP
df.PROC=data.PROC
df.iloc[:,1:6] = data.iloc[:,2:7]
for i in range(1,11):
    dr =  (data.iloc[i-1,2:7].sum()*data.iloc[i-1,7])+data.iloc[i-1,8]
    df.SUM.iloc[[i-1]] = dr
for i in range(1,6):
    df["O"+str(i)]=df["O"+str(i)]*df["PROC"]
dfO = df.sort_values(by="SUM",ascending=1).reset_index(drop=True)




df1 = dfO.iloc[:,1:6].T
df1.columns=dfO.iloc[:,0]
df2 = dfO.iloc[:,1:8].T
df2.columns=dfO.iloc[:,0]

print(df1)
print(df2)
siralama = {}
jobListe = dfO.iloc[:,0]
for i in range(int(df1.shape[1])) :
    dfDeneme = pd.DataFrame(df1.iloc[:,i])
    dfDeneme = dfDeneme.sort_values(by=list(dfDeneme)[0])
    liste = dfDeneme.index.tolist()
    liste2 = []
    for i in dfDeneme[list(dfDeneme)[0]]:
        liste1 = list(dfDeneme[list(dfDeneme)[0]])
        liste2 = list(dfDeneme[list(dfDeneme)[0]].index)
        for item in liste1:
            if item == 0:
                liste2.pop(liste1.index(item))
    siralama[list(dfDeneme)[0]] = liste2    
    



        # if i == 0:
        #     liste.remove(liste.index())
    # for i in liste
    # print(type(dfDeneme[list(dfDeneme)[0]] != 0))
    # siralama[list(dfDeneme)[0]] = liste


# for item in jobListe:
#     print(item,siralama[item])

def JobYukSirala(dfData,Liste,Job):
    # print(dfData,Liste,Job)
    listeOrderSure = []
    for i in liste:
        listeOrderSure.append((i,dfData.loc[str(i),str(Job)]))
    labels = ["Order","Value"]
    dataFrame = pd.DataFrame.from_records(listeOrderSure,columns=labels)
    dataFrame = dataFrame.sort_values(by="Value",ascending=1)
    # print(Job,list(dataFrame.loc[:,"Order"]))
    return list(dataFrame.loc[:,"Order"])


for i in range(len(jobListe),0,-1):
    if not i - 1 == 0:
        listeA = siralama[jobListe[i-1]]
        listeB = siralama[jobListe[i-2]]
        liste = []
        for a in listeB:
            for b in listeA:
                if a==b:
                    liste.append(a)
        if len(liste)>0:
            print("1-",jobListe[i-1],liste)
            liste = JobYukSirala(df2,listeA,jobListe[i-1])
            print("2-",jobListe[i-1],liste)
        if len(liste)>0:      
            for c in reversed(liste):
                listeA.remove(c)
                listeA.insert(0,c)
            
            siralama[jobListe[i-1]] = listeA


# for item in jobListe:
#     print(item,siralama[item])


toplam = 0
orderToplamListesi = {}
for order in range(1,6):
    orderToplamListesi.update({"O"+str(order):0})

def toplama(Order,Value):
    global toplam
    global orderToplamListesi
    orderToplamListesi[Order]=Value
    



for item in jobListe:
    toplam += df2.loc["SETUP",item]
    for i in siralama[item]:
        toplam += df2.loc[i,item]
        toplama(i,toplam)    

sayi = 0
for i in orderToplamListesi.values():
    sayi += i

print("Toplam",sayi)
    


# toplam = 0
# orderToplamListesi = {}
# for order in range(1,6):
#     orderToplamListesi.update({"O"+str(order):0})

# def ilerideVarmi(order,Job):
#     global jobListe
#     global siralama
#     liste = list(jobListe)
#     if liste.index(Job)+1  == len(liste):
#         return False
#     else:
#         sayi = liste.index(Job)
#         sinama  = False
#         for i in range(sayi,len(liste)):
#             for item in siralama[liste[i]] :
#                 if order in item:
#                     sinama = True
#         return sinama



# # print(list(jobListe))
# for item in jobListe:
#     toplam += df2.loc["SETUP",item]
#     for i in siralama[item]:
#         print(item,i,ilerideVarmi(i,item))
#         toplam += df2.loc[i,item]
#         if ilerideVarmi(i,item):            
#             orderToplamListesi[i] = toplam
#     print("Toplam",toplam)
# print(orderToplamListesi)
# sayi = 0
# for i in orderToplamListesi.values():
#     sayi += i

# print("Toplam",sayi)


                    






        # if list(set(siralama[jobListe[i-1]]) & set(siralama[jobListe[i-2]]))[0] > 0:
        #     print(siralama[jobListe[i-1]])
    


# print(df1.iloc[:,0])
# dfDeneme = pd.DataFrame(df1.iloc[:,0])
# dfDeneme.columns = ["J8"]
# # print(dfDeneme.sort_values(by=0))
# data = { "J8":dfDeneme.sort_values(by="J8") 
# }
# # dfDeneme = pd.DataFrame(df1.iloc[:,1])
# # data.update({"J5":dfDeneme.sort_values(by=1)})

# p = pd.Panel(data)
# print(p["J8"])






