from fastapi import FastAPI
from typing import Optional
import sqlite3
import pandas as pd
from pydantic import BaseModel



app = FastAPI(
    title="API del Settore del lavoro",
    description="Questa API fornisce dati sull lavoro e su eventuali campi delle tabelle.",
    version="1.0.0",
    contact={
        "name": "Lorenzo Prette",
        "email": "lorenzo.prette@edu.itspiemonte.it",
    },
)


#api per le tabelle principali

def connect_db(query:str,params:tuple = ()):
    conn = sqlite3.connect('lavoro.db')
    df = pd.read_sql_query(query,conn,params=params)
    conn.close()
    return df

@app.get("/incidenza_spese")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM incidenza_spese"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records') 


@app.get("/partecipazione_mercato_lavoro")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM partecipazione_mercato_lavoro"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')


@app.get("/tasso_sppravvivenza_imprese")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM tasso_sppravvivenza_imprese"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')


@app.get("/regioni")
def getIncidnezaSpese():
    query = "SELECT * FROM regioni"
    params = []

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')     

#api per le serie calcolate

@app.get("/incidenza_spese_media_aree")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM incidenza_spese_media_aree"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')


@app.get("/partecipazione_mercato_lavoro_media")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM partecipazione_mercato_lavoro_media"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')

@app.get("/partecipazione_mercato_lavoro_media_aree")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM partecipazione_mercato_lavoro_media_aree"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')

@app.get("/tasso_sppravvivenza_imprese_media")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM tasso_sppravvivenza_imprese_media"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')

@app.get("/tasso_sppravvivenza_imprese_media_aree")
def getIncidnezaSpese(da_anno:Optional[int] = None,a_anno:Optional[int]=None):
    query = "SELECT * FROM tasso_sppravvivenza_imprese_media_aree"
    params = []
    if da_anno and a_anno:
        query += " WHERE Anno BETWEEN ? AND ?"
        params.extend([da_anno, a_anno])

    df = connect_db(query, tuple(params))
    return df.to_dict(orient='records')


#api di inserimento 
class Prova(BaseModel):
    regione : str
    Anno: int
    Percentuale_spesa_imprese : float

@app.post('/insert')
def insert(item:Prova):
    #troviamo l'id della regione 
    conn = sqlite3.connect("lavoro.db",)
    cursor = conn.cursor()

    cursor.execute("SELECT id  FROM regioni WHERE Regione = ?",(item.regione,))
    result = cursor.fetchone()  

    if not result:
        return {"error":f"Regione '{item.regione}'non trovata nel database"}
    
    id_regione = result[0]

     # Costruisci dinamicamente la INSERT
    columns = ["regione_id "]
    values = [id_regione]
    placeholders = ["?"]

    if item.Anno is not None:
        columns.append("Anno")
        values.append(item.Anno)
        placeholders.append('?')

    if item.Percentuale_spesa_imprese is not None:
        columns.append("Percentuale_spesa_imprese")
        values.append(item.Percentuale_spesa_imprese)
        placeholders.append('?')


    query = f"INSERT INTO incidenza_spese  ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
    cursor.execute(query,values)
    conn.commit()
    conn.close()
    return {"message": "Inserimento riuscito", "dati_inseriti": dict(zip(columns, values))}



    



 