import pandas as pd
import sqlite3

conn = sqlite3.connect("lavoro.db")
cursor = conn.cursor()

#funzione per interpolazre i dati mancanti 
def interoplate_data(df,columns):
    for col in columns:
        df[col] = df[col].interpolate(method='linear')

    return df


#interpolazione dati mancanti 
for table,colums in [('incidenza_spese','Percentuale_spesa_imprese'),
                     ('partecipazione_mercato_lavoro','Percentuale_forze_lavoro_15_64_anni'),
                     ('tasso_sppravvivenza_imprese','Percentuale_sopravvivenza_imprese')]:
    
    df = pd.read_sql_query(f"SELECT * FROM {table}",conn)
    df = interoplate_data(df,[colums])
    df.to_sql(table,conn,if_exists='replace',index=False)