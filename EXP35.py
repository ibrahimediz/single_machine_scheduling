import sqlite3 as sql

db = sql.connect(r"D:\İbrahim EDİZ\SMS\single_machine_scheduling\PINAR.db")
cursor = db.cursor()
cursor.execute("""
SELECT  *
FROM V35_JOB_ORDER AS A
""")
# print(cursor.fetchall())
liste = []
for a,b in cursor.fetchall():
   
    sorgu = "SELECT "
    for k in range(1,6):
        sorgu += "O"+str(k)+"P,"
    sorgu = sorgu.rstrip(",")
    
    sorgu += " FROM V35_1 where JOB = '{}' "
    cursor.execute(sorgu.format(str(a)))
    kliste = [c for c in cursor.fetchall()[0]]
    liste.append(kliste)
# for item in liste:
#     item.sort()


print(*liste)