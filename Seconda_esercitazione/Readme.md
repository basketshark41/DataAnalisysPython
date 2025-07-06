# Comando per creare la venv

python -m venv venv

# Per lanciare la venv usare

.\venv\Scripts\Activate.ps1 

# Nel caso dia un errore sull'esecuzione dello script il problema più comune possono i permessi di windows quinid usare questo comando

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Una volta nella venv installare i pacchetti necesari all'esecuzione con il seguente comando 

pip install <nome_pacchetto>
Esempio: pip install fastapi pandas uvicorn

# Per lanciare l'app fastapi

Una volta entrati nella venv e anver installato tutti i pacchetti rihciesti usare il comando: 

- uvicorn <nome_script>:app --reload

se avete il vostro script all'interno di una cartella specifica usare:

- uvicorn <nome_cartella>.<nome_script>:app --reload