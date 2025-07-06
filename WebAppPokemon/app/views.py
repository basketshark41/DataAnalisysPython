from flask import Blueprint, render_template, Response
import io
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models import Pokemon, DatiPesca
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

@main.route('/grafico')
def grafico():
    # Esempio dati
    datiPesca = DatiPesca.query.all()
    prod_by_region = {}
    for d in datiPesca:
        if d.regione not in prod_by_region:
            prod_by_region[d.regione] = {'anno': [], 'produttivita': []}
        prod_by_region[d.regione]['anno'].append(d.anno)
        prod_by_region[d.regione]['produttivita'].append(d.produttivita)

    # Crea il grafico
    plt.figure(figsize=(12, 8))
    for regione, data in prod_by_region.items():
        plt.plot(data['anno'], data['produttivita'], label=regione)

    plt.xlabel("Anno")
    plt.ylabel("Produttività (migliaia €)")
    plt.title("Andamento della produttività del settore pesca per regione")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')
    
@main.route('/grafico/occupazione')
def grafico_occupazione_importanza():
    # Carica i dati dal database
    dati = DatiPesca.query.all()

    # Ristruttura i dati per regione
    data_by_region = {}
    for d in dati:
        reg = d.regione
        data_by_region.setdefault(reg, {'anno': [], 'occ': [], 'imp': []})
        data_by_region[reg]['anno'].append(d.anno)
        data_by_region[reg]['occ'].append(d.occupazione)
        data_by_region[reg]['imp'].append(d.importanza_economica)

    # Crea la figura
    plt.figure(figsize=(14, 8))
    for regione, vals in data_by_region.items():
        # linea occupazione
        plt.plot(vals['anno'], vals['occ'],
                 label=f"{regione} - Occupazione",
                 linestyle='-', marker='o')
        # linea importanza economica
        plt.plot(vals['anno'], vals['imp'],
                 label=f"{regione} - Import. Econ.",
                 linestyle='--', marker='x')

    plt.xlabel("Anno")
    plt.ylabel("Valore normalizzato")
    plt.title("Andamento Occupazione e Importanza Economica per Regione")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)
    plt.tight_layout()

    # Salva in buffer e ritorna come PNG
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')


@main.route('/grafico/hp')
def grafico_hp():
    pokemons = Pokemon.query.all()
    hp = [p.hp for p in pokemons if p.hp is not None]
    if not hp:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'Nessun dato HP disponibile', ha='center', va='center')
    else:
        fig, ax = plt.subplots()
        ax.hist(hp, bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Distribuzione HP Pokémon')
        ax.set_xlabel('HP')
        ax.set_ylabel('Numero Pokémon')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@main.route('/grafico/tipi')
def grafico_tipi():
    pokemons = Pokemon.query.all()
    type_counts = {}
    for p in pokemons:
        if p.type1:
            type_counts[p.type1] = type_counts.get(p.type1, 0) + 1
    labels = list(type_counts.keys())
    sizes = list(type_counts.values())
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribuzione dei tipi principali')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@main.route('/grafico/atkdef')
def grafico_atkdef():
    pokemons = Pokemon.query.all()
    attack = np.array([p.attack for p in pokemons])
    defense = np.array([p.defense for p in pokemons])

    sum_stats = attack + defense
    mean_sum = np.mean(sum_stats)
    std_sum = np.std(sum_stats)

    best_index = np.argmax(sum_stats)
    best_pokemon = pokemons[best_index]

    fig, ax = plt.subplots(figsize=(19, 13))

    colors = []
    for s in sum_stats:
        if s >= mean_sum + 2 * std_sum:
            colors.append('blue')
        elif s <= mean_sum - 2 * std_sum:
            colors.append('red')
        else:
            colors.append('gray')

    colors[best_index] = 'green'

    sizes = [50] * len(pokemons)
    sizes[best_index] = 150
    for i, c in enumerate(colors):
        if c in ['red', 'blue']:
            sizes[i] = 100

    ax.scatter(attack, defense, alpha=0.6, c=colors, s=sizes, edgecolor='black')

    # Annotazioni miglior Pokémon e outlier
    ax.annotate(best_pokemon.name,
                (attack[best_index], defense[best_index]),
                textcoords="offset points", xytext=(10,10),
                ha='left', fontsize=9, fontweight='bold', color='green')
    for i, c in enumerate(colors):
        if c in ['red', 'blue']:
            ax.annotate(pokemons[i].name,
                        (attack[i], defense[i]),
                        textcoords="offset points", xytext=(10,-10),
                        ha='left', fontsize=8, color=c)

    # Definisci range per disegnare linee
    x_vals = np.array(ax.get_xlim())

    # Linea media: attack + defense = mean_sum -> defense = mean_sum - attack
    ax.plot(x_vals, mean_sum - x_vals, color='black', linestyle='-', label='Media (somma attacco+difesa)')

    # Linee deviazione standard ±4
    ax.plot(x_vals, (mean_sum + 2*std_sum) - x_vals, color='blue', linestyle='--', label='+4 deviazioni standard')
    ax.plot(x_vals, (mean_sum - 2*std_sum) - x_vals, color='red', linestyle='--', label='-4 deviazioni standard')

    ax.set_title('Attacco vs Difesa')
    ax.set_xlabel('Attacco')
    ax.set_ylabel('Difesa')
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')

@main.route('/grafico/leggendari')
def grafico_legendari():
    pokemons = Pokemon.query.all()
    pokemons = [p for p in pokemons if getattr(p, 'legendary', False) is True]

    attack = np.array([p.attack for p in pokemons])
    defense = np.array([p.defense for p in pokemons])

    # Media e deviazione standard
    mean_attack, std_attack = attack.mean(), attack.std()
    mean_defense, std_defense = defense.mean(), defense.std()

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(attack, defense, alpha=0.5)

    # Trova gli outlier: quelli con attacco o difesa oltre 2 deviazioni standard dalla media
    outlier_mask = (
        (np.abs(attack - mean_attack) > 2 * std_attack) |
        (np.abs(defense - mean_defense) > 2 * std_defense)
    )

    # Evidenzia gli outlier in rosso
    ax.scatter(attack[outlier_mask], defense[outlier_mask], color='red', alpha=0.7)

    # Aggiungi i nomi dei Pokémon accanto ai pallini rossi (outlier)
    for i, p in enumerate(pokemons):
        if outlier_mask[i]:
            ax.annotate(p.name, (attack[i], defense[i]), textcoords="offset points", xytext=(5,5), ha='left')

    ax.set_title('Attacco vs Difesa dei leggendari (outlier in rosso)')
    ax.set_xlabel('Attacco')
    ax.set_ylabel('Difesa')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Response(buf.getvalue(), mimetype='image/png')