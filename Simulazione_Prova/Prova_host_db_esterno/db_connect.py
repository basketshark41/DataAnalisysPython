# pip install mysql-connector-python
import mysql.connector as mc

conn = mc.connect(
    host="traverandfriends-fintech2024prette.c.aivencloud.com",
    port="22185",
    user="avnadmin",
    password="AVNS_fCuGK2Q43LcaoHzrUqQ",
    database="ecommerce"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM utente")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()