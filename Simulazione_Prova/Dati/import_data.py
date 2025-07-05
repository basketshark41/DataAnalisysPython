import pandas as pd
import requests
import os
from io import StringIO
import sqlite3

# URL dei dataset
importanza_url = 'https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Importanza-economica-del-settore-della-pesca-per-regione.csv'
occupazione_url = 'https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Andamento-occupazione-del-settore-della-pesca-per-regione.csv'
produttivita_url = 'https://raw.githubusercontent.com/Lollo110204/DataAnalisysPython/refs/heads/main/Dati_csv/Produttivita-del-settore-della-pesca-per-regione.csv'

curr_dirr = os.getcwd()
csv_dir = os.path.join(curr_dirr,'csv')

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
    
def save_df_local(df, filename):
    os.makedirs(csv_dir, exist_ok=True)
    path = os.path.join(csv_dir, filename)
    df.to_csv(path, index=False, encoding='utf-8')
    print(f"DataFrame salvato in {path}")


df_importanza = import_data(importanza_url)
df_occupazione = import_data(occupazione_url)
df_produttività = import_data(produttivita_url)

save_df_local(df_importanza,'importanza.csv')
save_df_local(df_occupazione,'occupazione.csv')
save_df_local(df_produttività,'produttivita.csv')


df_importanza = df_importanza.rename(columns={'Percentuale valore aggiunto pesca-piscicoltura-servizi':'valore_aggiunto'})
df_occupazione = df_occupazione.rename(columns={'Variazione percentuale unitŕ di lavoro della pesca':'variazione_percentuale_lavoro_pesca'})
df_produttività = df_produttività.rename(columns={'Produttivitŕ in migliaia di euro':'poduttivita'})

# Funzione per normalizzare i dati mancanti tramite interpolazione
def interpolate_missing_data(df, columns):
    for col in columns:
        df[col] = df[col].interpolate(method='linear')
    return df


#connessione al db 
conn = sqlite3.connect('prova_esame.db')
cursor = conn.cursor()

# Inserimento dei dati nelle tabelle
for _, row in df_occupazione.iterrows():
    id_regione = cursor.execute("SELECT id FROM regioni WHERE nome = ?", (row['Regione'],)).fetchone()[0]
    cursor.execute('INSERT INTO occupazione_pesca (regione_id, anno, variazione_percentuale_lavoro_pesca) VALUES (?, ?, ?)',
                   (id_regione, row['Anno'],row['variazione_percentuale_lavoro_pesca']))
    
for _, row in df_importanza.iterrows():
    id_regione = cursor.execute("SELECT id FROM regioni WHERE nome = ?", (row['Regione'],)).fetchone()[0]
    cursor.execute('INSERT INTO importanza_pesca (regione_id, anno, valore_aggiunto) VALUES (?, ?, ?)',
                   (id_regione, row['Anno'],row['valore_aggiunto']))
    

for _, row in df_produttività.iterrows():
    id_regione = cursor.execute("SELECT id FROM regioni WHERE nome = ?", (row['Regione'],)).fetchone()[0]
    cursor.execute('INSERT INTO produttivita_pesca (regione_id, anno, poduttivita) VALUES (?, ?, ?)',
                   (id_regione, row['Anno'],row['poduttivita']))
    
 
conn.commit()
conn.close()





