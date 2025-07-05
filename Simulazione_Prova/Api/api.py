from fastapi import FastAPI
from typing import Optional
import sqlite3
import pandas as pd

app = FastAPI(
    title="API di prova per allenamento",
    description="Prove di API per allenamento.",
    version="1.0.0",
    contact={
        "name": "Prette Lorenzo",
        "email": "lorenzo.prette@edu.itspiemonte.it",
    }
)

def query_db(query:str,params: tuple = ()):
    conn = sqlite3.connect("prova_esame.db")
    df = pd.read_sql_query(query,conn,params=params)
    conn.close()
    return df


@app.get("/importanza")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM importanza_pesca "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/occupazione")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM occupazione_pesca "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/produttivita")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM produttivita_pesca "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/importanza_media_percentuale")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM importanza_media_percentuale "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/media_occupazione_aree_geografiche")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM media_occupazione_aree_geografiche "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/produttiva_totale_anno")
def prova_get(da_anno:Optional[int]=None, a_anno:Optional[int]=None):
    query = "SELECT *  FROM produttiva_totale_anno "
    params=[]
    if da_anno and a_anno:
        query += "WHERE anno BETWEEN ? and ?"
        params.extend([da_anno,a_anno])

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

@app.get("/regioni")
def prova_get():
    query = "SELECT *  FROM regioni"
    params=[]

    df = query_db(query,tuple(params))
    return df.to_dict(orient='records')

