import sqlite3
import pandas as pd

conn = sqlite3.connect("prova_esame.db")


# Funzione per interpolare i dati mancanti
def interpoazione_dati_mancanti(df,columns):
        for col in columns:
            df[col] = df[col].interpolate(method='linear')
        return df

# Interpolazione dei dati mancanti

for table, column in [('importanza_pesca','valore_aggiunto'),
                       ('occupazione_pesca','variazione_percentuale_lavoro_pesca'),
                        ('produttivita_pesca','poduttivita')]:
      df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
      df = interpoazione_dati_mancanti(df,[column])
      df.to_sql(table,conn,if_exists='replace',index=False)
    

conn.close()