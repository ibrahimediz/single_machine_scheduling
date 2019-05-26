import pandas as pd
import os
import time


class SMSCozum():
    kayit_adres = ""

    def __init__(self, is_adi, Folderadres, txt_adres, csv_adres, Job, Order, TopSure, DosyaSure, wSetup,kayit):
        self.is_adi = is_adi
        self.Folderadres = Folderadres
        self.txt_adres = txt_adres
        self.csv_adres = csv_adres
        self.Job = Job
        self.Order = Order
        self.TopSure = TopSure
        self.DosyaSure = DosyaSure
        self.wSetup = wSetup
        self.start = time.perf_counter()
        self.sutun = []
        self.data = None
        self.df = None
        self.dfO = None
        self.siralama = {}
        self.jobListe = []
        self.toplam = 0
        self.orderToplamListesi = {}
        self.ToplamSure = time.perf_counter()
        self.DosyaSure = time.perf_counter()
        self.OrderList = []
        self.kayit = kayit

    def sutunHazirla(self):
        OrderList=[]
        sutun = ["Job"]
        for i in range(1, self.Order + 1):
            sutun.append("O" + str(i))
            OrderList.append("O" + str(i))
        sutun += ["PROC", "SETUP"]
        return sutun,OrderList


    def sutunGuncelle(self,basliklar=[],Veri=""):
        return basliklar.append(Veri)


    def csvOkuDf(self,FolderAdres,csv_adres,delimiter):
        return pd.read_csv(FolderAdres+os.sep+csv_adres, delimiter=delimiter)

    def dosyaHazirla(self):
        self.sutun,self.OrderList = self.sutunHazirla()
        self.adres = self.Folderadres + "\\" + self.txt_adres
        self.data = self.csvOkuDf(self.Folderadres,self.csv_adres, ";")

        self.KayitTut("İlk Okuma", self.data)
        self.sutunGuncelle(self.sutun,"SUM")
        self.df = pd.DataFrame(columns=self.sutun)
        self.df.Job = self.data.Job
        if self.wSetup == 0:
            self.df.SETUP = 0
        else:
            self.df.SETUP = self.data.SETUP
        self.df.PROC = self.data.PROC
        self.df.iloc[:, 1:self.Order + 1] = self.data.iloc[:, 2:self.Order + 2]
        for i in range(1, self.Job + 1):
            dr = (self.data.iloc[i - 1, 2:self.Order + 2].sum() * self.data.iloc[i - 1, self.Order + 2]) + \
                 self.data.iloc[i - 1, self.Order + 3]
            self.df.SUM.iloc[[i - 1]] = dr
        for i in range(1, self.Order + 1):
            self.df["O" + str(i)] = self.df["O" + str(i)] * self.df["PROC"]
        self.dfO = self.df.sort_values(by="SUM", ascending=1).reset_index(drop=True)

        self.KayitTut("Sum Eklendi", self.dfO)

        self.Transpoze(self.dfO, self.Order)
        self.siralama, self.jobListe = self.SiralamaHazirla(self.df1, self.dfO)
        self.tekrarDuzenlemesiTekil()
        self.toplamaIslemi()
        if self.kayit:
            self.Ozet()






    def Transpoze(self, Kaynak, Order):
        self.df1 = self.df1Transpoze(Kaynak,Order)
        self.df2 = self.df2Transpoze(Kaynak,Order)




    def df1Transpoze(self,Kaynak,Order):
        df1 = Kaynak.iloc[:, 1:Order + 1].T
        df1.columns = Kaynak.iloc[:, 0]
        self.KayitTut("df1 Eklendi", df1)
        return df1


    def df2Transpoze(self,Kaynak,Order):
        df2 = Kaynak.iloc[:, 1:Order + 3].T
        df2.columns = Kaynak.iloc[:, 0]
        self.KayitTut("df2 Eklendi", df2)
        return df2

    def SiralamaHazirla(self, df, TemDf):
        siralamaSoz = {}
        jobListe = TemDf.iloc[:, 0]
        for i in range(int(df.shape[1])):
            dfDeneme = pd.DataFrame(df.iloc[:, i])
            dfDeneme = dfDeneme.sort_values(by=list(dfDeneme)[0])
            liste = dfDeneme.index.tolist()
            liste2 = []
            for i in dfDeneme[list(dfDeneme)[0]]:
                liste1 = list(dfDeneme[list(dfDeneme)[0]])
                liste2 = list(dfDeneme[list(dfDeneme)[0]].index)
                for item in liste1:
                    if item == 0:
                        liste2.pop(liste1.index(item))
            siralamaSoz[list(dfDeneme)[0]] = liste2
        self.KayitTut("JobListe Eklendi", jobListe)
        self.KayitTut("Sıralama Eklendi", siralamaSoz)
        return siralamaSoz, jobListe



    def tekrarsizlariBul(self, job, order):
        tekrar = False
        for i in range(0, len(self.jobListe)):
            if job != self.jobListe[i] and list(self.jobListe).index(job) < list(self.jobListe).index(self.jobListe[i]):
                if order in self.siralama[self.jobListe[i]]:
                        tekrar = True
        return tekrar

    def tekrarsizlariBulTum(self, job, order):
        tekrar = False
        for i in range(0, len(self.jobListe)):
            if job != self.jobListe[i]:
                if order in self.siralama[self.jobListe[i]]:
                    return True
        return tekrar



    def tekrarDuzenlemesiTekil(self):
        sozlukTekrar = {}
        for i in range(0, len(self.jobListe)):
            listeYalnizOrder = []
            for item in self.siralama[self.jobListe[i]]:
                if not self.tekrarsizlariBul(self.jobListe[i], item) and list(self.jobListe).index(self.jobListe[i]) != len(self.jobListe) - 1:
                    self.siralama[self.jobListe[i]].remove(item)
                    self.siralama[self.jobListe[i]].insert(0, item)
                if not self.tekrarsizlariBulTum(self.jobListe[i], item):
                    listeYalnizOrder.append(item)
            if len(listeYalnizOrder) > 0:
                sozlukTekrar.update({self.jobListe[i]: listeYalnizOrder})

        for i in list(self.jobListe):
            for item in self.siralama[i]:
                for key, value in sozlukTekrar.items():
                    if key == i:
                        for val in value:
                            if item == val:
                                if i == "J3":
                                    x = 1
                                self.siralama[i].remove(item)
                                self.siralama[i].insert(0, item)

    def orderToplamListesiOlustur(self,Order):
        orderToplamListesi = {}
        for order in range(1, Order + 1):
            orderToplamListesi.update({"O" + str(order): 0})
        return orderToplamListesi

    def toplamaIslemiBagimsiz(self,jobliste,orderSozluk,df,Order):
        ordertoplamalistesi = self.orderToplamListesiOlustur(Order)
        toplam = 0
        sayi = 0
        for item in jobliste:
            toplam += df.loc["SETUP", item]
            for i in orderSozluk[item]:
                toplam += df.loc[i, item]
                ordertoplamalistesi[i] = toplam
        for i in ordertoplamalistesi.values():
            sayi += i
        return sayi


    def toplamaIslemi(self):
        # self.tekrarDuzenlemesiTekil()
        self.orderToplamListesi = self.orderToplamListesiOlustur(self.Order)
        for item in self.jobListe:
            self.toplam += self.df2.loc["SETUP", item]
            for i in self.siralama[item]:
                self.toplam += self.df2.loc[i, item]
                self.toplama(i, self.toplam)
        self.KayitTut("orderToplamListesi Eklendi", self.orderToplamListesi)

    def Ozet(self):
        self.sayi = 0
        for i in self.orderToplamListesi.values():
            self.sayi += i
        print("Toplam Eklendi\n", self.is_adi, file=open(self.adres, "a"))
        print("Toplam", self.sayi, "Geçen Süre :", self.gecenSure(self.start), "sn", "\n" * 2, file=open(self.adres, "a"))
        print("Dosyada Geçen Süre :", self.gecenSure(self.DosyaSure), "sn", "\n" * 2, file=open(self.adres, "a"))
        print("Toplamda Geçen Süre :", self.gecenSure(self.TopSure), "sn", "\n" * 2, file=open(self.adres, "a"))
        print("Toplam", self.sayi, "Geçen Süre :", self.gecenSure(self.start), "sn")

    def toplama(self, Order, Value):
        self.orderToplamListesi[Order] = Value

    def KayitTut(self, mesaj, veri):
        if self.kayit:
            print(mesaj + "\n", self.is_adi, file=open(self.adres, "a"))
            print(veri, "\n" * 2, file=open(self.adres, "a"))

            print(mesaj + "\n", self.is_adi)
            print(veri, "\n" * 2)

    def gecenSure(self, start):
        return time.perf_counter() - start

    def orderListeGonder(self):
        return self.orderToplamListesi

    def jobListeGonder(self):
        return self.jobListe

    def SozluksiralamaGonder(self):
        return self.siralama

    def defaultSiralamaGonder(self):
        defaultSira = {}
        liste = []
        for item in range(1,self.Job+1):
            liste.append("J"+str(item))
        for eleman in liste:
            orderListe = []
            for i in range(1,self.Order+1):
                orderListe.append("O"+str(i))
            defaultSira.update({eleman:orderListe})
        return liste,defaultSira


    @classmethod
    def DosyaOlustur(cls):
        import os
        file = open("temp.txt", "w")
        try:
            if not os.path.exists(cls.adres):
                file = open(cls.adres, "w")
            else:
                file = open(cls.adres, "w")
        except Exception as Hata:
            file.write(str(Hata))
        finally:
            file.close()


def dosyaisimleri(sira):
    liste = []
    for i in range((sira * 25) + 1, (sira * 25) + 26):
        liste.append("Experiment" + str(i) + ".csv")
    return liste


if __name__ == "__main__":
    ToplamSure = time.perf_counter()
    DosyaSure = time.perf_counter()
    sira = 0
    for ord in range(5, 25, 5):
        for job in range(5, 25, 5):
            new_table_list = dosyaisimleri(sira)
            SMSCozum.kayit_adres = os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord,
                                                                                                           job) + "\\" + r"\I{}_J{}.txt".format(
                ord, job)
            SMSCozum.DosyaOlustur()
            for item in new_table_list:
                DosyaSure = time.perf_counter()
                istanim = SMSCozum(item.split(".")[0],
                                   os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord, job),
                                   r"\I{}_J{}_1.txt".format(ord, job), item, Job=job, Order=ord, TopSure=ToplamSure,
                                   DosyaSure=DosyaSure, wSetup=1,kayit=1)
                istanim.dosyaHazirla()
            sira += 1
