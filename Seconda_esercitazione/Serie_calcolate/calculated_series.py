import pandas as pd
import sqlite3


#per ora non utilizzato
def query_db(query: str, params: tuple = ()):
    conn = sqlite3.connect('pesca.db')
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df


conn = sqlite3.connect('lavoro.db')
cursor = conn.cursor()

#andiamo a recuperari i dari dal db
#query
df_incidenza_spese = pd.read_sql_query('SELECT * FROM incidenza_spese',conn)
df_partecipazione_mercato_lavoro= pd.read_sql_query('SELECT * FROM partecipazione_mercato_lavoro',conn)
df_tasso_sppravvivenza_imprese = pd.read_sql_query('SELECT * FROM tasso_sppravvivenza_imprese',conn)
df_regioni = pd.read_sql_query('SELECT * FROM regioni',conn)



#unione dei df per otterene le aree geografiche 
df_incidenza_spese=pd.merge(df_incidenza_spese,df_regioni,left_on='regione_id',right_on='id')
df_partecipazione_mercato_lavoro=pd.merge(df_partecipazione_mercato_lavoro,df_regioni,left_on='regione_id',right_on='id')
df_tasso_sppravvivenza_imprese=pd.merge(df_tasso_sppravvivenza_imprese,df_regioni,left_on='regione_id',right_on='id')
#per pulire i dati vado a droppare le colonne x_id e y_id dai df ottenuti siccome sono riferimenti agli indici delle due tabelle
df_incidenza_spese=df_incidenza_spese.drop(columns=['id_x','id_y'])
df_partecipazione_mercato_lavoro=df_partecipazione_mercato_lavoro.drop(columns=['id_x','id_y'])
df_tasso_sppravvivenza_imprese=df_tasso_sppravvivenza_imprese.drop(columns=['id_x','id_y'])

#Serie calcolate 
#1. Partecipazione popolazione al mercato del lavoro delle 5 Aree Nord-ovest, Nord-est, Centro, Sud, Isole
df_partecipazione_mercato_lavoro_media_aree = df_partecipazione_mercato_lavoro.groupby(['Anno','Area_geografica'])['Percentuale_forze_lavoro_15_64_anni'].mean().reset_index()
#2. Partecipazione popolazione al mercato del lavoro NAZIONALE
df_partecipazione_mercato_lavoro_media = df_partecipazione_mercato_lavoro.groupby('Anno')['Percentuale_forze_lavoro_15_64_anni'].mean().reset_index()
#3. Media incidenza spesa imprese in ricerca sviluppo delle 5 Aree Nord-ovest, Nord-est, Centro, Sud, Isole
df_incidenza_spese_media_aree = df_incidenza_spese.groupby(['Anno','Area_geografica'])['Percentuale_spesa_imprese'].mean().reset_index()
#4. Media tasso di sopravvivenza imprese alto tasso conoscenza NAZIONALE
df_tasso_sppravvivenza_imprese_media = df_tasso_sppravvivenza_imprese.groupby('Anno')['Percentuale_sopravvivenza_imprese'].mean().reset_index()
#5. Media tasso di sopravvivenza imprese alto tasso conoscenza delle 5 Aree Nord-ovest, Nord-est, Centro,Sud, Isole
df_tasso_sppravvivenza_imprese_media_aree = df_tasso_sppravvivenza_imprese.groupby(['Anno','Area_geografica'])['Percentuale_sopravvivenza_imprese'].mean().reset_index()

#print(df_tasso_sppravvivenza_imprese_media_aree)
#cursor.execute('''DROP TABLE incidenza_spese_media_aree''')
#inserimento delle serie calcolate nel db con eventuali tabelle
cursor.execute('''CREATE TABLE IF NOT EXISTS partecipazione_mercato_lavoro_media_aree ( Anno TEXT, Area_geografica TEXT, Percentuale_forze_lavoro_15_64_anni FLOAT,  PRIMARY KEY (Anno, Area_geografica))''')
df_partecipazione_mercato_lavoro_media_aree.to_sql('partecipazione_mercato_lavoro_media_aree',conn,if_exists='replace',index=False)
cursor.execute('''CREATE TABLE IF NOT EXISTS partecipazione_mercato_lavoro_media ( Anno TEXT, Percentuale_forze_lavoro_15_64_anni FLOAT,  PRIMARY KEY (Anno, Percentuale_forze_lavoro_15_64_anni))''')
df_partecipazione_mercato_lavoro_media.to_sql('partecipazione_mercato_lavoro_media',conn,if_exists='replace',index=False)
cursor.execute('''CREATE TABLE IF NOT EXISTS incidenza_spese_media_aree ( Anno TEXT,Area_geografica TEXT, Percentuale_spesa_imprese FLOAT,  PRIMARY KEY (Anno, Area_geografica))''')
df_incidenza_spese_media_aree.to_sql('incidenza_spese_media_aree',conn,if_exists='replace',index=False)
cursor.execute('''CREATE TABLE IF NOT EXISTS tasso_sppravvivenza_imprese_media ( Anno TEXT, Percentuale_sopravvivenza_imprese FLOAT,  PRIMARY KEY (Anno, Percentuale_sopravvivenza_imprese))''')
df_tasso_sppravvivenza_imprese_media.to_sql('tasso_sppravvivenza_imprese_media',conn,if_exists='replace',index=False)
cursor.execute('''CREATE TABLE IF NOT EXISTS tasso_sppravvivenza_imprese_media_aree ( Anno TEXT,Area_geografica TEXT, Percentuale_sopravvivenza_imprese FLOAT,  PRIMARY KEY (Anno, Area_geografica))''')
df_tasso_sppravvivenza_imprese_media_aree.to_sql('tasso_sppravvivenza_imprese_media_aree',conn,if_exists='replace',index=False)











