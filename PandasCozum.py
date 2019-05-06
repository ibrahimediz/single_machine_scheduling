# from os import listdir
# from os.path import isfile,join
# yol = r"E:\Projelerim\single_machine_scheduling\DENEME CSV SETLER\DENEME CSV SETLER\I=5, J=10"
# dosya = [f for f in listdir(yol) if isfile(join(yol,f))]

# print(dosya)
# input()

import pandas as pd
import numpy as np
import os
import time
def DosyaOlustur(adres):
    import os
    try:
        file=None
        if not os.path.exists(adres):
            file = open(adres,"w")
        else :
            file = open(adres,"r+")
    except Exception as Hata:
        file.write(str(Hata))
    finally:
        file.close()



def OkuBakalım(is_adi,Folderadres,txt_adres,csv_adres,Job,Order,TopSure,DosyaSure):
    start = time.perf_counter()
    def gecenSure(start):
        return time.perf_counter()-start
    sutun = ["Job"] 
    for i in range (1,Order+1):
        sutun.append("O"+str(i))
    sutun += ["PROC","SETUP"]
    adres = Folderadres+"\\"+txt_adres
    data =  pd.read_csv(Folderadres+"\\"+csv_adres,delimiter=";")
    DosyaOlustur(Folderadres+"\\"+txt_adres)
    
    print("İlk Okuma\n",is_adi,gecenSure(start),file = open(adres,"a"))
    print(data,"\n",is_adi,file = open(adres,"a"))


    print("İlk Okuma\n",is_adi,gecenSure(start))
    print(data,"\n",is_adi)
    
    sutun.append("SUM")
    df = pd.DataFrame(columns=sutun)
    df.Job = data.Job
    df.SETUP = data.SETUP
    df.PROC=data.PROC
    df.iloc[:,1:Order+1] = data.iloc[:,2:Order+2]
    for i in range(1,Job+1):
        dr =  (data.iloc[i-1,2:Order+2].sum()*data.iloc[i-1,Order+2])+data.iloc[i-1,Order+3]
        df.SUM.iloc[[i-1]] = dr
    for i in range(1,Order+1):
        df["O"+str(i)]=df["O"+str(i)]*df["PROC"]
    dfO = df.sort_values(by="SUM",ascending=1).reset_index(drop=True)

    print("Sum Eklendi\n",is_adi,file = open(adres,"a"))
    print(dfO,"\n"*2,file = open(adres,"a"))

    print("Sum Eklendi\n",is_adi)
    print(dfO,"\n"*2)

    df1 = dfO.iloc[:,1:Order+1].T
    df1.columns=dfO.iloc[:,0]

    print("df1 Eklendi\n",is_adi,file = open(adres,"a"))
    print(df1,"\n"*2,file = open(adres,"a"))

    print("df1 Eklendi\n",is_adi)
    print(df1,"\n"*2)

    df2 = dfO.iloc[:,1:Order+3].T
    df2.columns=dfO.iloc[:,0]

    print("df2 Eklendi\n",is_adi,file = open(adres,"a"))
    print(df2,"\n"*2,file = open(adres,"a"))

    print("df2 Eklendi\n",is_adi)
    print(df2,"\n"*2)

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


    print("JobListe Eklendi\n",is_adi,file = open(adres,"a"))
    print(jobListe,"\n"*2,file = open(adres,"a"))


    print("JobListe Eklendi\n",is_adi)
    print(jobListe,"\n"*2)
    

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




    # for i in range(len(jobListe),0,-1):
    #     if not i - 1 == 0:
    #         listeA = siralama[jobListe[i-1]]
    #         listeB = siralama[jobListe[i-2]]
    #         liste = []
    #         for a in listeB:
    #             for b in listeA:
    #                 if a==b:
    #                     liste.append(a)
    #         if len(liste)>0:
    #             liste = JobYukSirala(df2,listeA,jobListe[i-1])
    #             print("Fark Listesi-",jobListe[i-1],liste)
    #         if len(liste)>0:      
    #             for c in reversed(liste):
    #                 listeA.remove(c)
    #                 listeA.insert(0,c)
                
    #             siralama[jobListe[i-1]] = listeA

    print("Sıralama Eklendi\n",is_adi,file = open(adres,"a"))
    print(siralama,"\n"*2,file = open(adres,"a"))


    print("Sıralama Eklendi\n",is_adi)
    print(siralama,"\n"*2)

    def tekrarsizlariBul(job,order):
        tekrar = False
        for i in range(0,len(jobListe)):
            if job != jobListe[i]:
                if item in siralama[jobListe[i]]:
                    if order in item:
                        tekrar = True
        return tekrar

    for i in range(0,len(jobListe)):
        listeYalnizOrder = siralama[jobListe[i]]
        for item in listeYalnizOrder:
           if not tekrarsizlariBul(jobListe[i],item):
               listeYalnizOrder.remove(item)
               listeYalnizOrder.insert(0,item)

    print(siralama)        
            
            
    

    toplam = 0
    orderToplamListesi = {}
    for order in range(1,Order+1):
        orderToplamListesi.update({"O"+str(order):0})

    def toplama(Order,Value):
        orderToplamListesi[Order]=Value
        
    


    for item in jobListe:
        toplam += df2.loc["SETUP",item]
        for i in siralama[item]:
            toplam += df2.loc[i,item]
            toplama(i,toplam)


    print("orderToplamListesi Eklendi\n",is_adi,file = open(adres,"a"))
    print(orderToplamListesi,"\n"*2,file = open(adres,"a"))

    print("orderToplamListesi Eklendi\n",is_adi)
    print(orderToplamListesi,"\n"*2)


    sayi = 0
    for i in orderToplamListesi.values():
        sayi += i


    print("Toplam Eklendi\n",is_adi,file = open(adres,"a"))
    print("Toplam",sayi,"Geçen Süre :",gecenSure(start),"sn","\n"*2,file = open(adres,"a"))
    print("Dosyada Geçen Süre :",gecenSure(DosyaSure),"sn","\n"*2,file = open(adres,"a"))
    print("Toplamda Geçen Süre :",gecenSure(TopSure),"sn","\n"*2,file = open(adres,"a"))    
    print("Toplam",sayi,"Geçen Süre :",gecenSure(start),"sn")

    
        
table_list = []

def dosyaisimleri(sira):
    liste = []
    for i in range((sira*25)+1,(sira*25)+25):
        liste.append("Experiment"+str(i)+".csv")
    return liste



ToplamSure = time.perf_counter()
DosyaSure = time.perf_counter()
sira = 0
for ord in range(5,25,5):
    for job in range(5,25,5):
        new_table_list = dosyaisimleri(sira)
        for item in new_table_list:
            DosyaSure = time.perf_counter()
            OkuBakalım(item.split(".")[0],r"E:\Projelerim\single_machine_scheduling\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord,job),r"\I{}_J{}.txt".format(ord,job),item,Job=job,Order=ord,TopSure=ToplamSure,DosyaSure=DosyaSure)
        sira += 1        
# OkuBakalım("Exp_35",r"E:\Projelerim\single_machine_scheduling\DENEME CSV SETLER\DENEME CSV SETLER\I=5, J=5",r"\deneme.txt",r"Experiment4.csv",Job=5,Order=5,TopSure=ToplamSure,DosyaSure=DosyaSure)

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






