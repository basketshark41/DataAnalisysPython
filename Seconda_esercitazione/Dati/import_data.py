import pandas as pd 
import requests
from io import StringIO
import os
import sqlite3

#url dei csv
incidenza_spese_url = 'https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Incidenza-spesa-imprese-in-ricerca-e-sviluppo-per-regione.csv'
partecipazione_mercato_lavoro_url = 'https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Partecipazione-della-popolazione-al-mercato-del-lavoro-per-regione.csv'
tasso_sppravvivenza_imprese_url ='https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Tasso-sopravvivenza-imprese-alta-intensita-di-conoscenza-per-regione.csv'

#recupero la path corrente 
curr_dir = os.getcwd()
csv_dir = os.path.join(curr_dir,'csv')



# Funzione per importare e processare i dati
def import_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        csv_content = StringIO(response.text)
        df = pd.read_csv(csv_content, sep=';')
        df.columns = [col.replace('�', 'à') for col in df.columns]
        return df
    else:
        print(f"Errore nell'importazione dei dati da {url}")
        return None
    
df_incidenza_spese = import_data(incidenza_spese_url)
df_partecipazione_mercato_lavoro = import_data(partecipazione_mercato_lavoro_url)
df_tasso_sppravvivenza_imprese = import_data(tasso_sppravvivenza_imprese_url)

#rinominazione di alcune colonne
df_incidenza_spese = df_incidenza_spese.rename(columns={'Percentuale spesa imprese in ricerca e sviluppo':'Percentuale_spesa_imprese'})
df_partecipazione_mercato_lavoro = df_partecipazione_mercato_lavoro.rename(columns={'Percentuale forze di lavoro in etŕ 15-64 anni':'Percentuale_forze_lavoro_15_64_anni'})
df_tasso_sppravvivenza_imprese = df_tasso_sppravvivenza_imprese.rename(columns={'Percentuale sopravvivenza imprese alta conoscenza ':'Percentuale_sopravvivenza_imprese'})


#funzione per salvare i df in csv locali nell'eventualità di un'analisi 
def save_local_csv_from_df(df:pd.DataFrame,nome_file):
    directory = os.path.join(csv_dir,nome_file)
    return df.to_csv(directory,index=False)

save_local_csv_from_df(df_incidenza_spese,'incidenza_spese.csv')
save_local_csv_from_df(df_partecipazione_mercato_lavoro,'partecipazione_mercato_lavoro.csv')
save_local_csv_from_df(df_tasso_sppravvivenza_imprese,'tasso_sppravvivenza_imprese.csv')

#connessione al db per effettuare il recupero delle regioni cosi da unirle ai df speculari delle tabelle
conn = sqlite3.connect('lavoro.db')
cursor = conn.cursor()

df_regioni = pd.read_sql_query("SELECT * FROM regioni",conn)
save_local_csv_from_df(df_regioni,'regioni.csv')

# Unisco i due df usando il nome della regione
df_incidenza_spese = df_incidenza_spese.merge(df_regioni[['id', 'Regione']],
                         left_on='Regione',
                         right_on='Regione',
                         how='left')

df_partecipazione_mercato_lavoro = df_partecipazione_mercato_lavoro.merge(df_regioni[['id', 'Regione']],
                         left_on='Regione',
                         right_on='Regione',
                         how='left')

df_tasso_sppravvivenza_imprese = df_tasso_sppravvivenza_imprese.merge(df_regioni[['id', 'Regione']],
                         left_on='Regione',
                         right_on='Regione',
                         how='left')


# print(df_incidenza_spese)
# print(df_partecipazione_mercato_lavoro)
# print(df_tasso_sppravvivenza_imprese)

for _, row in df_incidenza_spese.iterrows():
    cursor.execute('INSERT INTO incidenza_spese (regione_id, Anno ,Percentuale_spesa_imprese) VALUES (?, ?, ?)',
                  (row['id'],row['Anno'],row['Percentuale_spesa_imprese']))
    
for _, row in df_partecipazione_mercato_lavoro.iterrows():
    cursor.execute('INSERT INTO partecipazione_mercato_lavoro (regione_id, Anno ,Percentuale_forze_lavoro_15_64_anni) VALUES (?, ?, ?)',
                  (row['id'],row['Anno'],row['Percentuale_forze_lavoro_15_64_anni']))
    
for _, row in df_tasso_sppravvivenza_imprese.iterrows():
    cursor.execute('INSERT INTO tasso_sppravvivenza_imprese (regione_id, Anno ,Percentuale_sopravvivenza_imprese) VALUES (?, ?, ?)',
                  (row['id'],row['Anno'],row['Percentuale_sopravvivenza_imprese']))
    

conn.commit()
conn.close()
