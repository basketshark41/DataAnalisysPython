# Comandi
# 1. Clonare il progetto o scompattare la cartella
cd WebAppPokemon

# 2. Creare e attivare un virtual environment
python -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 3. Installare le dipendenze
pip install -r requirements.txt

# 4. Creare il database (se richiesto)
python setup_db.py

# Impostare variabili d’ambiente Flask
export FLASK_APP=run.py
export FLASK_ENV=development  # (opzionale per debug)

# Eseguire il server
flask run

# Attivare venv se non lo è già
source venv/bin/activate

# Controllare errori nei file
python -m py_compile app/*.py app/utils/*.py

# Verificare importazioni mancanti o errori linter (opzionale)
pip install pylint
pylint app/

# Creazione ambiente virtuale
python -m venv venv

# Attivazione ambiente virtuale
source venv/bin/activate         # Linux/macOS
venv\Scripts\activate.bat        # Windows

# Disattivare ambiente virtuale
deactivate


# Installare un pacchetto
pip install nome_pacchetto

# Salvare i pacchetti in requirements.txt
pip freeze > requirements.txt

# Installare da requirements.txt
pip install -r requirements.txt

# Disinstallare un pacchetto
pip uninstall nome_pacchetto

# Verificare pacchetti installati
pip list

# Eseguire test con unittest (built-in)
python -m unittest discover

# Eseguire test con pytest (più moderno)
pytest

# Debug interattivo (inserito nel codice)
import pdb; pdb.set_trace()

# Controllo sintassi / linting
pylint nomefile.py
flake8 nomefile.py

# Format del codice
black nomefile.py
isort nomefile.py  # Ordina gli import

# Verifica errori statici con mypy
mypy nomefile.py

# Eseguire uno script Python
python script.py

# Eseguire un modulo come script
python -m nome_modulo
python -m http.server 8000    # Esempio: server HTTP locale


# Avviare una REPL interattiva
python

# Avviare IPython se installato
ipython

# Mostrare documentazione di un modulo
python -m pydoc nome_modulo

# Compilare file .py in .pyc
python -m compileall .


# Eseguire script che elabora un CSV
python analizza_csv.py data/Pokemon.csv

# Stampare JSON formattato
cat file.json | python -m json.tool


# Estensioni VS Code consigliate per progetti Python / Flask

## 🐍 Essenziali per Python
ms-python.python
ms-python.vscode-pylance
ms-toolsai.jupyter
cstrap.flask-snippets

## 🔧 Linting, Formatting, Refactoring
ms-python.black-formatter
ms-python.isort
ms-python.flake8
njpwerner.autodocstring
kevinrose.vsc-python-indent

## 🧪 Testing, Debug e Profilazione
littlefoxteam.vscode-python-test-adapter
formulahendry.code-runner
almenon.arepl

## 🌐 HTML / CSS / JS Supporto
ritwickdey.LiveServer
ecmel.vscode-html-css
xabikos.JavaScriptSnippets
esbenp.prettier-vscode

## 🧠 AI & Auto-complete (opzionali)
GitHub.copilot
kiteco.kite

## 🛠 Dev Tools & Utility
mikestead.dotenv
humao.rest-client
christian-kohler.path-intellisense
CoenraadS.bracket-pair-colorizer-2


# PANDAS
# Da CSV
df = pd.read_csv("data.csv")

# Da dizionario
data = {'Nome': ['Pikachu', 'Bulbasaur'], 'Tipo': ['Elettro', 'Erba']}
df = pd.DataFrame(data)

df.head()         # Prime 5 righe
df.tail(3)        # Ultime 3 righe
df.shape          # (righe, colonne)
df.columns        # Nomi delle colonne
df.info()         # Info generali (tipi, null)
df.describe()     # Statistiche numeriche

# Colonne
df["Nome"]
df[["Nome", "Tipo"]]

# Righe per posizione o etichetta
df.iloc[0]        # Prima riga (posizione)
df.loc[0]         # Prima riga (etichetta)

# Filtri
df[df["Tipo"] == "Fuoco"]
df[df["Punti"] > 50]

# Ordinamento
df.sort_values(by="Punti", ascending=False)

# Raggruppamento
df.groupby("Tipo").mean()
df.groupby("Tipo").count()

# Aggiungere nuova colonna
df["Attacco"] = [50, 70]

# Rinominare colonne
df.rename(columns={"Nome": "Pokemon"})

# Eliminare colonne/righe
df.drop(columns="Tipo")
df.drop(index=0)

df.isnull()               # Mappa booleana
df.isnull().sum()         # Conteggio per colonna
df.dropna()               # Elimina righe con NaN
df.fillna(0)              # Sostituisce NaN con 0

df["Totale"] = df["Attacco"] + df["Difesa"]
df["Rapporto"] = df["Attacco"] / df["Difesa"]

# Trasformare valori con una funzione
df["Tipo"] = df["Tipo"].apply(lambda x: x.upper())

# Applicare funzione riga per riga
def classifica(row):
    return "Forte" if row["Totale"] > 100 else "Debole"

df["Classe"] = df.apply(classifica, axis=1)

# Concatenazione verticale
pd.concat([df1, df2])

# Merge stile SQL
pd.merge(df1, df2, on="ID", how="inner")  # left, right, outer

df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx")
df.to_json("output.json")


df.nunique()             # Valori unici per colonna
df.value_counts()        # Frequenze
df.sample(5)             # Campione casuale
df.duplicated()          # Duplicati
df.corr()                # Correlazione tra colonne numeriche

# MATPLOTLIB

x = [1, 2, 3, 4]
y = [10, 20, 25, 30]

plt.plot(x, y)
plt.title("Grafico semplice")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()

plt.plot(x, y)

plt.scatter(x, y)

plt.bar(x, y)
plt.barh(x, y)  # Barre orizzontali

plt.hist([1, 2, 2, 3, 4, 4, 4, 5], bins=5)

labels = ['Fuoco', 'Erba', 'Acqua']
sizes = [30, 40, 30]
plt.pie(sizes, labels=labels, autopct="%1.1f%%")


plt.title("Titolo del Grafico")
plt.xlabel("Asse X")
plt.ylabel("Asse Y")
plt.legend(["Legenda"])
plt.grid(True)


plt.plot(x, y, color='red', linestyle='--', marker='o')

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Con oggetto Axes")

fig, axs = plt.subplots(2, 2)  # 2x2 griglia
axs[0, 0].plot(x, y)
axs[0, 1].bar(x, y)
axs[1, 0].scatter(x, y)
axs[1, 1].hist(y)

plt.savefig("grafico.png")             # PNG
plt.savefig("grafico.pdf", dpi=300)    # PDF con alta risoluzione

plt.xlim(0, 100)             # Limiti asse X
plt.ylim(0, 50)              # Limiti asse Y
plt.xticks(rotation=45)      # Rotazione etichette X
plt.annotate("Pikachu", xy=(3, 25), xytext=(4, 30),
             arrowprops=dict(arrowstyle="->"))


# GRAFICI UTILI


## linee

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dati.csv", parse_dates=["Data"])
df = df.sort_values("Data")

plt.figure(figsize=(10, 5))
plt.plot(df["Data"], df["Valore"], label="Valore", color='blue')
plt.title("Andamento nel tempo")
plt.xlabel("Data")
plt.ylabel("Valore")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

## Grafico con media mobile (trend)

df["MediaMobile"] = df["Valore"].rolling(window=7).mean()

plt.plot(df["Data"], df["Valore"], alpha=0.4, label="Valore Giornaliero")
plt.plot(df["Data"], df["MediaMobile"], label="Media Mobile 7gg", color="red")

## Grafico a barre per somma per mese/anno

df["AnnoMese"] = df["Data"].dt.to_period("M")
df_grouped = df.groupby("AnnoMese")["Valore"].sum()

df_grouped.plot(kind="bar", figsize=(12, 5), color="skyblue")
plt.title("Valore Totale per Mese")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Boxplot per confrontare stagionalità / anni

df["Mese"] = df["Data"].dt.month

plt.figure(figsize=(10, 5))
df.boxplot(column="Valore", by="Mese")
plt.title("Distribuzione Mensile")
plt.suptitle("")
plt.xlabel("Mese")
plt.ylabel("Valore")
plt.show()

## Heatmap per pattern giornalieri / mensili

import seaborn as sns

df["Anno"] = df["Data"].dt.year
df["Mese"] = df["Data"].dt.month

pivot = df.pivot_table(index="Mese", columns="Anno", values="Valore", aggfunc="mean")

plt.figure(figsize=(10, 6))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title("Valore medio per mese/anno")
plt.show()

## Grafico con eventi / annotazioni

plt.plot(df["Data"], df["Valore"])
plt.axvline(pd.to_datetime("2023-03-01"), color='red', linestyle='--')
plt.text(pd.to_datetime("2023-03-01"), df["Valore"].max(), "Evento X", rotation=90)

## Multipli line plot (es. confronto categorie)

for tipo, gruppo in df.groupby("Categoria"):
    plt.plot(gruppo["Data"], gruppo["Valore"], label=tipo)

plt.legend()