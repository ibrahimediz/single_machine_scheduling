from SMSClassCozum2 import SMSCozum
import pandas as pd
import numpy as np
import os

class TabuSearch():
    def __init__(self):
        self.jobListe = None
        self.OrderList = None
        self.initialOrder = None
        self.TabuLongList1 = []
        self.TabuLongList2 = []
        self.TabuLongList3 = []
        self.TabuShortList = None
        self.TabuMediumList = None
        self.initialSolution()

    def RandomizeJobList(self,jobListe):
        import random as rnd
        liste = jobListe
        for i in liste:
           sayi = liste.index(i)
           yerlesim =  rnd.randint(0,len(liste))
           liste.remove(i)
           liste.insert(yerlesim,i)

    def initialSolution(self):
        import time
        # new_table_list = dosyaisimleri(sira)
        new_table_list = ["Experiment301.csv"]
        self.job = 5
        self.ord = 20
        SMSCozum.kayit_adres = os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(self.ord, self.job) + "\\" + r"\I{}_J{}.txt".format(
            self.ord, self.job)
        SMSCozum.DosyaOlustur()
        for item in new_table_list:
            DosyaSure = time.perf_counter()
            ToplamSure = time.perf_counter()
            self.istanim = SMSCozum(item.split(".")[0],
                               os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(self.ord, self.job),
                               r"\I{}_J{}_Tabu.txt".format(self.ord, self.job), item, Job=self.job, Order=self.ord, TopSure=ToplamSure,
                               DosyaSure=DosyaSure, wSetup=1, kayit=0)
            self.istanim.dosyaHazirla()

        self.OrderList = self.istanim.orderListeGonder()
        self.initialOrder = self.istanim.SozluksiralamaGonder()
        self.dfT = self.istanim.df2
        self.dfB = self.istanim.dfO
        self.jobListe,self.initialOrder = self.istanim.defaultSiralamaGonder()

    def readFrame(self):
        print(self.dfB)

    def orderListeGuncelle(self,orderListeSozluk = {}):
        gonderilecek = {}
        for key,value in orderListeSozluk.items():
            deneme = self.RandomizeOrderListe(value)
            gonderilecek.update({key:deneme})
        return gonderilecek


    def RandomizeOrderListe(self,orderListe):
        import random as rnd
        rndliste = orderListe.copy()
        for item in rndliste:
            sayi = rndliste.index(item)
            yeniyer = rnd.randint(0,len(rndliste))
            rndliste.remove(item)
            rndliste.insert(yeniyer,item)
        return rndliste

    def CalculateCT(self,jobliste,OrderListe):
        result = self.istanim.toplamaIslemiBagimsiz(jobliste,OrderListe,self.dfT, self.ord)
        print(result)
        return result

    def SameOrderSize(self):
        pass

    def donumSayisi(self,n):
        return n*self.fakHesapla(n-1)
    def fakHesapla(self,n):
        sayi = 1
        for i in range(1,n+1):
            sayi *= i
        return sayi


    def OrderChange(self):
        pass

if __name__ == "__main__":
    deneme = TabuSearch()
    # print(deneme.initialOrder)
    # print(deneme.dfB)
    deneme.istanim.Ozet()
    customSolutionResult = deneme.istanim.sayi
    print(deneme.jobListe)
    print(deneme.initialOrder)
    customSolutionResult = deneme.CalculateCT(deneme.jobListe, deneme.initialOrder)
    print(deneme.CalculateCT(deneme.jobListe, deneme.initialOrder))
    # print(deneme.donumSayisi(len(list(deneme.jobListe))))
    # mevcut = 0
    # for i in list(deneme.jobListe):
    #    mevcut += len(deneme.initialOrder[i])
    # print(deneme.donumSayisi(mevcut))



    for adim in range(0,1500):
        liste = list(deneme.jobListe).copy()
        # print(liste)
        deneme.RandomizeJobList(liste)
        liste2 = liste.copy()
        deneme.RandomizeJobList(liste2)
        # print(liste)
        sonuc = deneme.CalculateCT(liste,deneme.initialOrder)
        if sonuc < customSolutionResult:
            # deneme.TabuLongList1.append([liste,sonuc,deneme.initialOrder])
            if not sonuc in deneme.TabuLongList1:
                deneme.TabuLongList1.append(sonuc)
            print(adim, sonuc)
        OrderSozluk =  deneme.orderListeGuncelle(deneme.initialOrder)
        # print(deneme.initialOrder)
        # print(OrderSozluk)
        sonuc = deneme.CalculateCT(list(deneme.jobListe),OrderSozluk)
        if sonuc < customSolutionResult:
            # deneme.TabuLongList2.append([list(deneme.jobListe),sonuc,OrderSozluk])
            if not sonuc in deneme.TabuLongList2:
                deneme.TabuLongList2.append(sonuc)
            print(adim, sonuc)
        sonuc = deneme.CalculateCT(liste,OrderSozluk)
        if sonuc < customSolutionResult:
            # deneme.TabuLongList3.append([liste, sonuc, OrderSozluk])
            if not sonuc in deneme.TabuLongList3:
                deneme.TabuLongList3.append(sonuc)
            print(adim, sonuc)
    print(deneme.istanim.Ozet())
    print(len(deneme.TabuLongList1))
    print(deneme.TabuLongList1)
    print(len(deneme.TabuLongList2))
    print(deneme.TabuLongList2)
    print(len(deneme.TabuLongList3))
    print(deneme.TabuLongList3)



