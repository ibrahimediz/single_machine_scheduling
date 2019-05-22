import os
import time
import pandas as pd
import numpy as np


class SMSClass(Order=0, Job=0, Folderadres="", txt_adres="",is_adi="",wSetup=1):
    def __init__(self):
        self.Order = Order
        self.Job = Job
        self.sutun = []
        self.Folderadres = Folderadres
        self.txt_adres = txt_adres
        self.adres = Folderadres + os.sep + txt_adres
        self.is_adi = is_adi
        self.data = None
        self.df = None
        self.df1 = None
        self.df2 = None
        self.df3 = None
        self.wSetup = wSetup
        self.ilkVeriOku()
        self.start = time.perf_counter()
        self.siralama = {}
        self.JobListe = []
        self.listeOrderSure = []
        self.sozlukTekrar = {}




    def ilkVeriOku(self):
        self.data = pd.read_csv(self.adres, delimiter=";")
        print("İlk Okuma\n", self.is_adi, self.gecenSure(self.start), file=open(self.adres, "a"))
        print(self.data, "\n", self.is_adi, file=open(self.adres, "a"))


    def SumHesaplaEkle(self):
        self.sutun.append("SUM")
        self.df = pd.DataFrame(columns=self.sutun)
        self.df.Job = self.data.Job
        if self.wSetup == 0:
            self.df.SETUP = 0
        else:
            self.df.SETUP = self.data.SETUP
        self.df.PROC = self.data.PROC
        self.df.iloc[:, 1:self.Order + 1] = self.data.iloc[:, 2:self.Order + 2]
        for i in range(1, self.Job + 1):
            dr = (self.data.iloc[i - 1, 2:self.Order + 2].sum() * self.data.iloc[i - 1, self.Order + 2]) + self.data.iloc[i - 1, self.Order + 3]
            self.df.SUM.iloc[[i - 1]] = dr
        for i in range(1, self.Order + 1):
            self.df["O" + str(i)] = df["O" + str(i)] * df["PROC"]
        self.dfO = self.df.sort_values(by="SUM", ascending=1).reset_index(drop=True)

        print("Sum Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print(self.dfO, "\n" * 2, file=open(self.adres, "a"))

        print("Sum Eklendi\n", self.is_adi)
        print(self.dfO, "\n" * 2)

    def transPoze(self):
        self.df1 = self.dfO.iloc[:, 1:self.Order + 1].T
        self.df1.columns = self.dfO.iloc[:, 0]

        print("df1 Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print(self.df1, "\n" * 2, file=open(self.adres, "a"))

        print("df1 Eklendi\n", self.is_adi)
        print(self.df1, "\n" * 2)

        self.df2 = self.dfO.iloc[:, 1:self.Order + 3].T
        self.df2.columns = self.dfO.iloc[:, 0]

        print("df2 Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print(self.df2, "\n" * 2, file=open(self.adres, "a"))

        print("df2 Eklendi\n", self.is_adi)
        print(self.df2, "\n" * 2)

        self.jobListe = self.dfO.iloc[:, 0]

        for i in range(int(self.df1.shape[1])):
            self.df3 = pd.DataFrame(self.df1.iloc[:, i])
            self.df3 = self.df3.sort_values(by=list(self.df3)[0])
            self.liste = self.df3.index.tolist()
            liste2 = []
            for i in self.df3[list(self.df3)[0]]:
                liste1 = list(self.df3[list(self.df3)[0]])
                liste2 = list(self.df3[list(self.df3)[0]].index)
                for item in liste1:
                    if item == 0:
                        liste2.pop(liste1.index(item))
            self.siralama[list(self.df3)[0]] = liste2

        print("JobListe Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print(self.jobListe, "\n" * 2, file=open(self.adres, "a"))

        print("JobListe Eklendi\n", self.is_adi)
        print(self.jobListe, "\n" * 2)

        print("Sıralama Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print(self.siralama, "\n" * 2, file=open(adres, "a"))

        print("Sıralama Eklendi\n", self.is_adi)
        print(self.siralama, "\n" * 2)

    def JobYukSirala(self,dfData,Liste,Job):
        # print(dfData,Liste,Job)

        for i in Liste:
            self.listeOrderSure.append((i, dfData.loc[str(i),str(self.Job)]))
        labels = ["Order","Value"]
        dataFrame = pd.DataFrame.from_records(self.listeOrderSure,columns=labels)
        dataFrame = dataFrame.sort_values(by="Value", ascending=1)
        # print(Job,list(dataFrame.loc[:,"Order"]))
        return list(dataFrame.loc[:, "Order"])

    def tekrarsizlariBul(self,job,order):
        if self.is_adi == "Experiment4" and job=="J4":
            print("x")
        tekrar = False
        for i in range(0,len(self.jobListe)):
            if job != self.jobListe[i] and list(self.jobListe).index(job) < list(self.jobListe).index(self.jobListe[i]):
                if item in self.siralama[self.jobListe[i]]:
                    if order in item:
                        tekrar = True
        return tekrar

    def tekrarsizlariBulTum(job,order):
        tekrar = False
        for i in range(0,len(jobListe)):
            if job != jobListe[i]:
                if item in siralama[jobListe[i]]:
                    if order in item:
                       return True
        return tekrar

    def dosyaOlustur(self):
        import os
        file = open("temp.txt", "w")
        try:
            if not os.path.exists(self.adres):
                file = open(self.adres, "w")
            else:
                file = open(self.adres, "w")
        except Exception as hata:
            file.write(str(hata))
        finally:
            file.close()

    def gecenSure(start):
        return time.perf_counter() - start

    def sutunOlustur(self):
        self.sutun = ["Job"]
        for i in range(1, self.Order + 1):
            self.sutun.append("O" + str(i))
        self.sutun += ["PROC", "SETUP"]
