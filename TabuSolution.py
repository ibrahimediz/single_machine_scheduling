from SMSClassCozum2 import SMSCozum
import os
import pandas as pd

class TabuSearch():
    def __init__(self):
        self.jobListe = None
        self.OrderList = None
        self.initialOrder = None
        self.initialSolution()


    # 14465
    # 15203
    # 1. Tabu Süresi Belirle
    # 2. Tabu İterasyon Sayısı Belirle
    # 3. Faz1 i uygula
    # 4. Bulduklarını kısa süreli hafızaya kaydet
    # 5. uzun süreli hafızaya ve orta süreliye
    # 5. Faz2 i uygula
    # 6. Bulduklarını kısa süreli hafızaya kaydet

    def initialSolution(self):
        import time
        # new_table_list = dosyaisimleri(sira)
        new_table_list = ["Experiment6.csv"]
        self.RepFileName = "Experiment6.csv"
        self.job = 5
        self.ord = 5
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
        self.dfT1 = self.istanim.df1
        self.dfB = self.istanim.dfO
        self.initialOrder, self.jobListe = self.istanim.SiralamaHazirla(self.dfT1, self.dfB)
        self.istanim.tekrarDuzenlemesiTekil()
        self.jobListe = self.istanim.jobListeGonder()

        # self.OrderList = self.istanim.orderListeGonder()
        # self.initialOrder = self.istanim.SozluksiralamaGonder()
        # self.dfT = self.istanim.df2
        # self.dfB = self.istanim.dfO
        # self.jobListe,self.initialOrder = self.istanim.defaultSiralamaGonder()

    def CalculateCT(self,jobliste,OrderListe):
        result = self.istanim.toplamaIslemiBagimsiz(jobliste,OrderListe,self.dfT, self.ord)
        # print(result)
        return result

class TabuAlg1():
    def __init__(self,JobList,Order,Procindx):
        self.JobList = JobList
        self.Order = Order
        self.Procindx = Procindx
        self.RandomizeJobList()
        self.resultSetAlg1 = self.GetValues()

    def RandomizeJobList(self):
        import random as rnd
        rndliste = self.JobList.copy()
        for item in rndliste:
            sayi = rndliste.index(item)
            yeniyer = rnd.randint(0,len(rndliste))
            rndliste.remove(item)
            rndliste.insert(yeniyer,item)
        self.JobList = rndliste.copy()

    def GetValues(self):
        CalculateTool = TabuSearch()
        return self.JobList,CalculateTool.CalculateCT(self.JobList, self.Order),self.Procindx


class TabuAlg2():
    def __init__(self,JobList,Order,Procindx):
        self.JobList = JobList
        self.Order = Order
        self.Procindx = Procindx
        self.Order = self.RandomizeOrder(self.Order)
        self.resultSetAlg2 = self.GetValues()

    def RandomizeOrderListe(self, orderListe):
        import random as rnd
        rndliste = orderListe.copy()
        for item in rndliste:
            sayi = rndliste.index(item)
            yeniyer = rnd.randint(0, len(rndliste))
            rndliste.remove(item)
            rndliste.insert(yeniyer, item)
        return rndliste

    def RandomizeOrder(self,orderListeSozluk = {}):
        gonderilecek = {}
        for key,value in orderListeSozluk.items():
            deneme = self.RandomizeOrderListe(value)
            gonderilecek.update({key:deneme})
        return gonderilecek

    def GetValues(self):
        CalculateTool = TabuSearch()
        return self.JobList,self.Order,CalculateTool.CalculateCT(self.JobList,self.Order),self.Procindx


class TabuAlg3():
    def __init__(self,JobList,Order,Procindx):
        self.JobList = JobList
        self.Order = Order
        self.Procindx = Procindx
        self.tekrarDuzenlemesiTekil()
        self.resultSetAlg3 = self.GetValues()

    def tekrarsizlariBul(self, job, order):
        tekrar = False
        for i in range(0, len(self.JobList)):
            if job != self.JobList[i] and list(self.JobList).index(job) < list(self.JobList).index(self.JobList[i]):
                if order in self.Order[self.JobList[i]]:
                    tekrar = True
        return tekrar

    def tekrarsizlariBulTum(self, job, order):
        tekrar = False
        for i in range(0, len(self.JobList)):
            if job != self.JobList[i]:
                if order in self.Order[self.JobList[i]]:
                    return True
        return tekrar

    def tekrarDuzenlemesiTekil(self):
        sozlukTekrar = {}
        for i in range(0, len(self.JobList)):
            listeYalnizOrder = []
            for item in self.Order[self.JobList[i]]:
                if not self.tekrarsizlariBul(self.JobList[i], item) and list(self.JobList).index(
                        self.JobList[i]) != len(self.JobList) - 1:
                    self.Order[self.JobList[i]].remove(item)
                    self.Order[self.JobList[i]].insert(0, item)
                if not self.tekrarsizlariBulTum(self.JobList[i], item):
                    listeYalnizOrder.append(item)
            if len(listeYalnizOrder) > 0:
                sozlukTekrar.update({self.JobList[i]: listeYalnizOrder})

        for i in list(self.JobList):
            for item in self.Order[i]:
                for key, value in sozlukTekrar.items():
                    if key == i:
                        for val in value:
                            if item == val:
                                if i == "J3":
                                    x = 1
                                self.Order[i].remove(item)
                                self.Order[i].insert(0, item)
    def GetValues(self):
        CalculateTool = TabuSearch()
        return self.JobList,self.Order,CalculateTool.CalculateCT(self.JobList,self.Order),self.Procindx




class TabuRun():
    def __init__(self):
        FirstRun = TabuSearch()
        self.FileName = FirstRun.RepFileName
        self.initialJobList = list(FirstRun.jobListe)
        self.initialOrder = FirstRun.initialOrder
        self.TabuLongTerm = []
        self.TabAlg = []
        self.TabAlg2 = []
        self.TabAlg3 = []
        self.df = None
        self.df2 = pd.DataFrame({"a": [123]})
        self.df3 = None
        self.dfResult = pd.DataFrame({"a": [123]})
        self.RunAlg1()



    def RunAlg1(self):
        for i in range(0,120):
            self.TabAlg.append(TabuAlg1(self.initialJobList,self.initialOrder,i).resultSetAlg1)
            self.EliminateResultsAlg1()

    def RunAlg2(self):
        listeler = list(self.df["JobList"])
        for item in listeler:
            i = 0
            while len(self.df2.index) < 30:
                    self.TabAlg2.append(TabuAlg2(item,self.initialOrder,i).resultSetAlg2)
                    self.EliminateResultsAlg2()
            i+=1
            # self.df2 = self.df2.sort_values(by=["CT"]).reset_index(drop=True)
            # for i in range(0,len(self.df2.index)):
            #     self.TabuLongList(self.df2.iloc[i]["JobList"],self.df2.iloc[i]["OrderList"],self.df2.iloc[i]["CT"])

    def RunAlg3(self):
        OrderList = list(self.df2["OrderList"])
        listeler = list(self.df2["JobList"])
        for li in listeler:
            for item in OrderList:
                self.TabAlg3.append(TabuAlg3(li,item,0).resultSetAlg3)
                self.EliminateResultsAlg3()



    def EliminateResultsAlg3(self):
        ProcindxS = []
        genelListe = []
        genelOrder = []
        CalcT = []
        for JobList,Order,CT,Procindx in self.TabAlg3:
            genelOrder.append(Order)
            for i in self.TabAlg3:
                devam = True
                for key,values in i[1].items():
                    if Order[key] == values and len(Order[key])>1:
                        genelOrder.remove(Order)
                        devam = False
                        break
                if devam:
                    genelOrder.append(Order)
                    genelListe.append(JobList)
                    CalcT.append(CT)
                    ProcindxS.append(Procindx)
            self.df3 = pd.DataFrame({"JobList": genelListe,"OrderList":genelOrder ,"CT": CalcT})
        self.df3 =self.df3.drop_duplicates("CT")
        self.df3 = self.df3.sort_values(by=["CT"])


    def EliminateResultsAlg2(self):
        ProcindxS = []
        genelListe = []
        genelOrder = []
        CalcT = []
        adim = 0
        for JobList,Order,CT,Procindx in self.TabAlg2:
            if not adim:
                genelOrder.append(Order)
                genelListe.append(JobList)
                CalcT.append(CT)
                ProcindxS.append(Procindx)
                adim = 1
            for i in genelOrder:
                devam = True
                for key,values in i.items():
                    if Order[key] == values and len(Order[key])>1:
                        devam = False
                        break
                if devam:
                    genelOrder.append(Order)
                    genelListe.append(JobList)
                    CalcT.append(CT)
                    ProcindxS.append(Procindx)
            self.df2 = pd.DataFrame({"JobList": genelListe,"OrderList":genelOrder ,"CT": CalcT})
            self.df2 = self.df2.drop_duplicates("CT")
            self.df2 = self.df2.sort_values(by=["CT"])
            print(self.df2)

    # def TabuLongList(self,JobList,Order,CT):
    #     genelListe = []
    #     genelOrder = []
    #     CalcT = []
    #     self.dfTemp = None
    #     if not len(self.dfResult.index) > 5:
    #         genelOrder.append(Order)
    #         genelListe.append(JobList)
    #         CalcT.append(CT)
    #         self.dfTemp = {"JobList": JobList,"OrderList":Order ,"CT": CT}
    #         self.dfResult = self.dfResult.append(self.dfTemp)
    #     else:
    #         self.dfResult = self.dfResult.sort_values(by=["CT"]).reset_index(drop=True)
    #         self.dfResult.drop(5)
    #         self.dfTemp = {"JobList": JobList, "OrderList": Order, "CT": CT}
    #         self.dfResult = self.dfResult.append(self.dfTemp)
    #         self.dfResult = self.dfResult.sort_index()







    def EliminateResultsAlg1(self):
        JobSoz = {}
        ProcindxS = []
        genelListe = []
        CalcT = []
        for JobList,CT,Procindx in self.TabAlg:
            ProcindxS.append(Procindx)
            genelListe.append(JobList)
            CalcT.append(CT)
            self.df = pd.DataFrame({"JobList": genelListe, "CT": CalcT})
            print(self.df)
        self.df["JobList_str"] = self.df["JobList"].astype(str)
        self.df = self.df.drop_duplicates("JobList_str")
        self.df = self.df.sort_values(by=["CT"])
        self.df = self.df.head(len(genelListe[0])*(len(genelListe[0])-1))




Run1 = TabuRun()
print(Run1.df)
Run1.RunAlg2()
Run1.df2.to_csv(Run1.FileName+".csv",sep=';', encoding='utf-8')

# Run1.RunAlg3()
# print(Run1.df3)







