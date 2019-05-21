from SMSClassCozum2 import SMSCozum
import pandas as pd
import numpy as np
import os

class TabuSearch():
    def __init__(self):
        self.jobListe = None
        self.OrderList = None
        self.initialOrder = None
        self.TabuLongList = None
        self.TabuShortList = None
        self.TabuMediumList = None
        self.initialSolution()


    def initialSolution(self):
        import time
        # new_table_list = dosyaisimleri(sira)
        new_table_list = ["Experiment1.csv"]
        job = 5
        ord = 5
        SMSCozum.kayit_adres = os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord,
                                                                                                       job) + "\\" + r"\I{}_J{}.txt".format(
            ord, job)
        SMSCozum.DosyaOlustur()
        for item in new_table_list:
            DosyaSure = time.perf_counter()
            ToplamSure = time.perf_counter()
            istanim = SMSCozum(item.split(".")[0],
                               os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord, job),
                               r"\I{}_J{}_Tabu.txt".format(ord, job), item, Job=job, Order=ord, TopSure=ToplamSure,
                               DosyaSure=DosyaSure, wSetup=1, kayit=0)
            istanim.dosyaHazirla()
        self.jobListe = istanim.jobListeGonder()
        self.OrderList = istanim.orderListeGonder()
        self.initialOrder = istanim.SozluksiralamaGonder()
        self.dfT = istanim.df2
        self.dfB = istanim.dfO

    def readFrame(self):
        pass

    def CalculateCT(self):
        pass

    def RandomizeJobs(self):
        pass

    def SameOrderSize(self):
        pass

    def OrderChange(self):
        pass

if __name__ == "__main__":
    deneme = TabuSearch()
    print(deneme.initialOrder)
    print(deneme.dfB)
