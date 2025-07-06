from flask import Blueprint, render_template, Response
import io
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from app.models import Pokemon, DatiPesca
import numpy as np
import seaborn as sns

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('dashboard.html')

@main.route('/genera-grafici')
def genera_tutti_grafici():
    """Genera tutti i grafici e li salva nella cartella static/graphs"""
    
    # Assicurati che la cartella esista
    graphs_dir = os.path.join('app', 'static', 'graphs')
    os.makedirs(graphs_dir, exist_ok=True)
    
    # Genera tutti i grafici
    grafico()
    grafico_occupazione_importanza()
    grafico_hp()
    grafico_tipi()
    grafico_atkdef()
    grafico_legendari()
    grafico_importanza_economica_barre()
    grafico_produttivita_evoluzione()
    grafico_heatmap_variazioni()
    grafico_radar_top_regioni()
    
    return "Tutti i grafici sono stati generati e salvati in static/graphs/"

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
    
    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'produttivita_pesca.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/produttivita_pesca.png"
    
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

    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'occupazione_importanza.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/occupazione_importanza.png"

@main.route('/grafico/importanza-barre')
def grafico_importanza_economica_barre():
    """Grafico a barre delle regioni con maggiore importanza economica media"""
    dati = DatiPesca.query.all()
    
    # Calcola l'importanza economica media per regione
    importanza_media = {}
    for d in dati:
        if d.regione not in importanza_media:
            importanza_media[d.regione] = []
        importanza_media[d.regione].append(d.importanza_economica)
    
    # Calcola la media per ogni regione
    regioni = []
    medie = []
    for regione, valori in importanza_media.items():
        if valori:  # Se ci sono valori
            regioni.append(regione)
            medie.append(np.mean(valori))
    
    # Ordina per importanza decrescente e prendi le top 10
    sorted_data = sorted(zip(regioni, medie), key=lambda x: x[1], reverse=True)[:10]
    regioni_top = [x[0] for x in sorted_data]
    medie_top = [x[1] for x in sorted_data]
    
    # Crea il grafico
    plt.figure(figsize=(12, 8))
    colors = plt.cm.viridis(np.linspace(0, 1, len(regioni_top)))
    bars = plt.bar(regioni_top, medie_top, color=colors, alpha=0.7)
    
    # Aggiungi i valori sulle barre
    for bar, valore in zip(bars, medie_top):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{valore:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Regione')
    plt.ylabel('Importanza Economica Media')
    plt.title('Top 10 Regioni per Importanza Economica del Settore Pesca')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salva il grafico
    graph_path = os.path.join('app', 'static', 'graphs', 'importanza_economica_barre.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/importanza_economica_barre.png"

@main.route('/grafico/produttivita-evoluzione')
def grafico_produttivita_evoluzione():
    """Grafico dell'evoluzione temporale della produttività media nazionale"""
    dati = DatiPesca.query.all()
    
    # Raggruppa per anno e calcola la media nazionale
    produttivita_annuale = {}
    for d in dati:
        if d.anno not in produttivita_annuale:
            produttivita_annuale[d.anno] = []
        produttivita_annuale[d.anno].append(d.produttivita)
    
    anni = sorted(produttivita_annuale.keys())
    medie_nazionali = [np.mean(produttivita_annuale[anno]) for anno in anni]
    
    # Calcola la tendenza lineare
    z = np.polyfit(anni, medie_nazionali, 1)
    p = np.poly1d(z)
    trend_line = p(anni)
    
    # Crea il grafico
    plt.figure(figsize=(12, 8))
    plt.plot(anni, medie_nazionali, 'o-', linewidth=2, markersize=8, 
             label='Produttività Media Nazionale', color='blue')
    plt.plot(anni, trend_line, '--', color='red', linewidth=2, 
             label=f'Tendenza (y = {z[0]:.2f}x + {z[1]:.2f})')
    
    plt.fill_between(anni, medie_nazionali, alpha=0.3, color='blue')
    plt.xlabel('Anno')
    plt.ylabel('Produttività Media (migliaia €)')
    plt.title('Evoluzione della Produttività Media Nazionale del Settore Pesca')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Salva il grafico
    graph_path = os.path.join('app', 'static', 'graphs', 'produttivita_evoluzione.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/produttivita_evoluzione.png"

@main.route('/grafico/heatmap-variazioni')
def grafico_heatmap_variazioni():
    """Grafico a heatmap delle variazioni percentuali per regione e anno"""
    dati = DatiPesca.query.all()
    
    # Crea una matrice delle variazioni percentuali
    regioni = list(set([d.regione for d in dati]))
    anni = sorted(list(set([d.anno for d in dati])))
    
    # Crea una matrice vuota
    matrix = np.zeros((len(regioni), len(anni)))
    
    # Popola la matrice con le variazioni percentuali (usando occupazione come proxy)
    for d in dati:
        if d.regione in regioni and d.anno in anni:
            row = regioni.index(d.regione)
            col = anni.index(d.anno)
            matrix[row, col] = d.occupazione
    
    # Crea il heatmap
    plt.figure(figsize=(16, 10))
    sns.heatmap(matrix, 
                xticklabels=anni, 
                yticklabels=regioni,
                cmap='RdYlBu_r',
                center=0,
                annot=True,
                fmt='.2f',
                cbar_kws={'label': 'Variazione Percentuale'})
    
    plt.title('Heatmap delle Variazioni Percentuali per Regione e Anno')
    plt.xlabel('Anno')
    plt.ylabel('Regione')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salva il grafico
    graph_path = os.path.join('app', 'static', 'graphs', 'heatmap_variazioni.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/heatmap_variazioni.png"

@main.route('/grafico/radar-top-regioni')
def grafico_radar_top_regioni():
    """Grafico a radar delle performance delle top 5 regioni"""
    dati = DatiPesca.query.all()
    
    # Calcola le metriche medie per regione
    metriche_regioni = {}
    for d in dati:
        if d.regione not in metriche_regioni:
            metriche_regioni[d.regione] = {'prod': [], 'occ': [], 'imp': []}
        metriche_regioni[d.regione]['prod'].append(d.produttivita)
        metriche_regioni[d.regione]['occ'].append(d.occupazione)
        metriche_regioni[d.regione]['imp'].append(d.importanza_economica)
    
    # Calcola le medie e trova le top 5 per produttività
    regioni_scores = []
    for regione, metriche in metriche_regioni.items():
        if metriche['prod']:  # Se ci sono dati
            score_prod = np.mean(metriche['prod'])
            score_occ = np.mean(metriche['occ'])
            score_imp = np.mean(metriche['imp'])
            regioni_scores.append((regione, score_prod, score_occ, score_imp))
    
    # Ordina per produttività e prendi le top 5
    top_5 = sorted(regioni_scores, key=lambda x: x[1], reverse=True)[:5]
    
    # Prepara i dati per il radar
    categorie = ['Produttività', 'Occupazione', 'Importanza Economica']
    N = len(categorie)
    
    # Normalizza i valori per il radar (0-1)
    max_prod = max([x[1] for x in top_5])
    max_occ = max([x[2] for x in top_5])
    max_imp = max([x[3] for x in top_5])
    
    # Crea il grafico radar
    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(projection='polar'))
    
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # Chiudi il poligono
    
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i, (regione, prod, occ, imp) in enumerate(top_5):
        values = [prod/max_prod, occ/max_occ, imp/max_imp]
        values += values[:1]  # Chiudi il poligono
        
        ax.plot(angles, values, 'o-', linewidth=2, label=regione, color=colors[i])
        ax.fill(angles, values, alpha=0.1, color=colors[i])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categorie)
    ax.set_ylim(0, 1)
    ax.set_title('Performance Radar delle Top 5 Regioni', size=16, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.grid(True)
    
    # Salva il grafico
    graph_path = os.path.join('app', 'static', 'graphs', 'radar_top_regioni.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return "Grafico salvato in static/graphs/radar_top_regioni.png"

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
    
    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'hp_distribution.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return "Grafico salvato in static/graphs/hp_distribution.png"

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
    
    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'tipi_distribution.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return "Grafico salvato in static/graphs/tipi_distribution.png"

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

    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'atk_def_scatter.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return "Grafico salvato in static/graphs/atk_def_scatter.png"

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

    # Salva il grafico nella cartella static/graphs
    graph_path = os.path.join('app', 'static', 'graphs', 'legendari_scatter.png')
    plt.savefig(graph_path, format='png', dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return "Grafico salvato in static/graphs/legendari_scatter.png"