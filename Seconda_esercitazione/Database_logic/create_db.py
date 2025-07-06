import sqlite3
import pandas

conn = sqlite3.connect("lavoro.db")
cursor = conn.cursor()

cursor.execute('''  
    CREATE TABLE IF NOT EXISTS regioni(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               Regione TEXT,
               Area_geografica TEXT
               )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidenza_spese(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               regione_id INTEGER,
               Anno INT,
               Percentuale_spesa_imprese FLOAT,

               FOREIGN KEY (regione_id) REFERENCES  regioni(id)
               )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS partecipazione_mercato_lavoro(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               regione_id INTEGER,
               Anno INT,
               Percentuale_forze_lavoro_15_64_anni FLOAT,

               FOREIGN KEY (regione_id) REFERENCES  regioni(id)
               )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasso_sppravvivenza_imprese(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               regione_id INTEGER,
               Anno INT,
               Percentuale_sopravvivenza_imprese FLOAT,

               FOREIGN KEY (regione_id) REFERENCES  regioni(id)
               )
''')


regioni = [('Valle d\'Aosta', 'Nord-ovest'),
           ('Piemonte', 'Nord-ovest'),
           ('Liguria', 'Nord-ovest'),
           ('Lombardia', 'Nord-ovest'),
           ('Trentino-Alto Adige', 'Nord-est'),
           ('Veneto', 'Nord-est'),
           ('Friuli-Venezia Giulia', 'Nord-est'),
           ('Emilia-Romagna', 'Nord-est'),
           ('Toscana', 'Centro'),
           ('Umbria', 'Centro'),
           ('Marche', 'Centro'),
           ('Lazio', 'Centro'),
           ('Abruzzo', 'Centro'),
           ('Molise', 'Sud'),
           ('Campania', 'Sud'),
           ('Puglia', 'Sud'),
           ('Basilicata', 'Sud'),
           ('Calabria', 'Sud'),
           ('Sicilia', 'Isole'),
           ('Sardegna', 'Isole')]


cursor.executemany('INSERT INTO regioni (Regione,Area_geografica) VALUES (?, ?)',regioni)

conn.commit()
conn.close()