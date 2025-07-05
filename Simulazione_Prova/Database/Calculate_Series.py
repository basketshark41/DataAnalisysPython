import sqlite3
import pandas as pd



def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect('prova_esame.db')
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df





#connessione al db
conn = sqlite3.connect('prova_esame.db')
cursor = conn.cursor()



# Query per ottenere i dati necessari
query_produttivita = "SELECT * FROM produttivita_pesca"
query_occupazione = "SELECT * FROM occupazione_pesca"
query_importanza = "SELECT * FROM importanza_pesca"
querry_regioni = "SELECT * FROM regioni"


#creazione dei df che uniscono area geografica con la regione effettiva
df_produttiva = query_db(query_produttivita)
df_occupazione = query_db(query_occupazione)
df_importanza = query_db(query_importanza)
df_regioni = query_db(querry_regioni)

df_produttiva = pd.merge(df_produttiva,df_regioni,left_on='regione_id',right_on='id')
df_occupazione = pd.merge(df_occupazione,df_regioni,left_on='regione_id',right_on='id')
df_importanza = pd.merge(df_importanza,df_regioni,left_on='regione_id',right_on='id')
#durante il merge viene creato un campo id_y che non serve e indica l'id dell'altra colonna cosa che non voglio e quindi droppo
df_produttiva = df_produttiva.drop(columns=['id_y','id_x'])
df_occupazione = df_occupazione.drop(columns=['id_y','id_x'])
df_importanza = df_importanza.drop(columns=['id_y','id_x'])



#Produttività totale in migliaia di euro delle 5 Aree Nord-ovest, Nord-est, Centro, Sud, Isole
df_produttiva_totale_anno = df_produttiva.groupby(['area_geografica','anno'])['poduttivita'].sum().reset_index()
#Produttività totale in migliaia di euro NAZIONALE
df_produttiva_totale = df_produttiva.groupby('anno')['poduttivita'].sum().reset_index()
# Media percentuale valore aggiunto pesca piscicoltura delle 5 Aree Nord-ovest, Nord-est,Centro, Sud, Isole
df_importanza_media_percentuale = df_importanza.groupby(['anno','area_geografica'])['valore_aggiunto'].mean().reset_index()
# Media Variazione percentuale occupazione NAZIONALE
df_media_occupazione = df_occupazione.groupby('anno')['variazione_percentuale_lavoro_pesca'].mean().reset_index()
# Media Variazione percentuale occupazione delle 5 Aree Nord-ovest, Nord-est, Centro,Sud, Isole
df_media_occupazione_aree_geografiche = df_occupazione.groupby(['anno','area_geografica'])['variazione_percentuale_lavoro_pesca'].mean().reset_index()

print(df_media_occupazione_aree_geografiche)


#creazione più inserimento dei dati nel db
cursor.execute('''

CREATE TABLE IF NOT EXISTS produttiva_totale_anno(
               
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               area_geografica TEXT,
               anno int,
               poduttivita FLOAT
               
               )

''')

df_produttiva_totale_anno.to_sql('produttiva_totale_anno',conn,if_exists='replace',index=False)



cursor.execute('''

CREATE TABLE IF NOT EXISTS produttiva_totale(
               
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               anno int,
               poduttivita FLOAT
               
               )

''')

df_produttiva_totale.to_sql('produttiva_totale',conn,if_exists='replace',index=False)

cursor.execute('''

CREATE TABLE IF NOT EXISTS importanza_media_percentuale(
               
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               anno int,
               area_geografica TEXT,
               valore_aggiunto FLOAT
               
               )

''')

df_importanza_media_percentuale.to_sql('importanza_media_percentuale',conn,if_exists='replace',index=False)

cursor.execute('''

CREATE TABLE IF NOT EXISTS media_occupazione(
               
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               anno int,
               variazione_percentuale_lavoro_pesca FLOAT
               
               )

''')

df_media_occupazione.to_sql('media_occupazione',conn,if_exists='replace',index=False)

cursor.execute('''

CREATE TABLE IF NOT EXISTS media_occupazione_aree_geografiche(
               
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               anno int,
               area_geografica TEXT
               variazione_percentuale_lavoro_pesca FLOAT
               
               )

''')

df_media_occupazione_aree_geografiche.to_sql('media_occupazione_aree_geografiche',conn,if_exists='replace',index=False)



# cursor.execute('''DROP TABLE produttiva_totale_anno''')
# cursor.execute('''DROP TABLE produttiva_totale''')
# cursor.execute('''DROP TABLE importanza_media_percentuale''')
# cursor.execute('''DROP TABLE media_occupazione''')

conn.close()