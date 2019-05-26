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
        # print(result)
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

class TabuLongTerm(TabuSearch):
    TabuLongList1 = []
    TabuSonucList = []
    TabLongOrderSozluk = {}
    def __init__(self,param=[],initial=0):
        self.initial = initial
        self.TabLongJobList = param[1]
        self.TabLongOrderSozluk = param[2]
        self.TabuLongTest(param)
        self.TabuLongMedCalc()



    def TabuLongResult(self,sonuc=0):
        if sonuc < self.initial:
            if len(self.TabuSonucList) < 10:
                self.TabuSonucList.append(sonuc)
            else:
                for item in self.TabuSonucList:
                    if item[0] > sonuc:
                        self.TabuSonucList.remove(item)
                        self.TabuSonucList.append(sonuc)
                    break

    def TabuLongTest(self,param=[]):
        if param[0] < self.initial:
            if len(self.TabuLongList1) < 10:
                self.TabuLongList1.append(param)
            else:
                for item in self.TabuLongList1:
                    if item[0] > param[0]:
                        self.TabuLongList1.remove(item)
                        self.TabuLongList1.append(param)
                    break

    def TabuLongMedCalc(self):
        TabuMed = TabuMedTerm(self.TabLongJobList,self.TabLongOrderSozluk)
        # OrderSozluk = deneme.orderListeGuncelle(self.TabuOrderSozluk)
        # sonuc = deneme.CalculateCT(self.TabJobList,OrderSozluk)
        # self.TabuLongResult(sonuc)






class TabuMedTerm(TabuLongTerm):

    def __init__(self,longTerm,longOrder):
        self.longTerm = longTerm
        self.TabuMediumList = []
        self.longOrder = longOrder
        self.TabuMedResult()


    def TabuMedResult(self):
        Phase2List = []
        for adim in range(0,1):
            OrderSozluk = self.RandomizeOrder(self.longOrder)
            print(OrderSozluk)
            Phase2List.append([self.longTerm,OrderSozluk])


        for item in Phase2List:
            sonuc = TabuSearch.CalculateCT(item[0],item[1])
            print(sonuc)
            self.TabuMediumTest(sonuc)

    def RandomizeOrder(self,orderListeSozluk = {}):
        gonderilecek = {}
        for key,value in orderListeSozluk.items():
            deneme = self.RandomizeOrderListe(value)
            gonderilecek.update({key:deneme})
        return gonderilecek

    def TabuMediumTest(self,param):
        if len(self.TabuSonucList) < 10 and self.initial:
            self.TabuSonucList.append(param)
        else:
            for item in self.TabuSonucList:
                if item[0] > param[0]:
                    self.TabuSonucList.remove(item)
                    self.TabuSonucList.append(param)
                break


class TabuShortTerm:
    def __init__(self,longTerm,MediumTerm):
        self.longTerm = longTerm
        self.MediumTerm = MediumTerm
        self.TabuShortList = []

    def TabuShortTest(self,param=[]):
        if len(self.TabuShortList) < 10:
            self.TabuShortList.append(param)
        else:
            for item in self.TabuShortList:
                if item[0] > param[0]:
                    self.TabuShortList.remove(item)
                    self.TabuShortList.append(param)
                    break



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
    Phase1List = []
    liste = list(deneme.jobListe).copy()
    for adim in range(0, len(deneme.jobListe)*1):
          deneme.RandomizeJobList(liste)
          while liste not in Phase1List:
              Phase1List.append(liste.copy())
    # print(*Phase1List,sep="\n")
    for item in Phase1List:
        sonuc = deneme.CalculateCT(item, deneme.initialOrder)
        TabuLong = TabuLongTerm([sonuc,item,deneme.initialOrder],customSolutionResult)

    # son = []
    # for h in TabuLongTerm.TabuLongList1:
    #     son.extend(h)
    # sonListe = list(set(son))
    # print(sonListe)

    print(TabuLongTerm.TabuSonucList)

          # for i in TabuLong.TabuLongList1:
          #     for adimOrder in range(0,1500):
          #         TabuMed = TabuMedTerm(i)
          #         OrderSozluk = deneme.orderListeGuncelle(deneme.initialOrder)
          #         sonuc = deneme.CalculateCT(liste,OrderSozluk)
          #         TabuMed.TabuMediumTest([sonuc, liste, OrderSozluk])














    #     if sonuc < customSolutionResult:
    #         # deneme.TabuLongList1.append([liste,sonuc,deneme.initialOrder])
    #         if not sonuc in deneme.TabuLongList1:
    #             deneme.TabuLongList1.append(sonuc)
    #         print(adim, sonuc)
    #     OrderSozluk =  deneme.orderListeGuncelle(deneme.initialOrder)
    #     # print(deneme.initialOrder)
    #     # print(OrderSozluk)
    #     sonuc = deneme.CalculateCT(list(deneme.jobListe),OrderSozluk)
    #     if sonuc < customSolutionResult:
    #         # deneme.TabuLongList2.append([list(deneme.jobListe),sonuc,OrderSozluk])
    #         if not sonuc in deneme.TabuLongList2:
    #             deneme.TabuLongList2.append(sonuc)
    #         print(adim, sonuc)
    #     sonuc = deneme.CalculateCT(liste,OrderSozluk)
    #     if sonuc < customSolutionResult:
    #         # deneme.TabuLongList3.append([liste, sonuc, OrderSozluk])
    #         if not sonuc in deneme.TabuLongList3:
    #             deneme.TabuLongList3.append(sonuc)
    #         print(adim, sonuc)
    # print(deneme.istanim.Ozet())
    # print(len(deneme.TabuLongList1))
    # print(deneme.TabuLongList1)
    # print(len(deneme.TabuLongList2))
    # print(deneme.TabuLongList2)
    # print(len(deneme.TabuLongList3))
    # print(deneme.TabuLongList3)



