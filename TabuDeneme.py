from SMSClassCozum2 import SMSCozum
import os

ToplamSure = time.perf_counter()
DosyaSure = time.perf_counter()
sira = 0
ord = 5
job = 5
item = "Experiment1.csv"
istanim = SMSCozum(item.split(".")[0],
                   os.getcwd() + r"\DENEME CSV SETLER\DENEME CSV SETLER\I={}, J={}".format(ord, job),
                   r"\I{}_J{}.txt".format("Tabu", "Deneme"), item, Job=job, Order=ord, TopSure=ToplamSure,
                   DosyaSure=DosyaSure, wSetup=1)
istanim.dosyaHazirla()
