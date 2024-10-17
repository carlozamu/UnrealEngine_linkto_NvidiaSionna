
# Progetto di Simulazione della Propagazione del Segnale in un Digital Twin

## Descrizione del progetto

Questo progetto mira a simulare la propagazione del segnale wireless in un ambiente urbano utilizzando un digital twin, creato attraverso l'integrazione di **Unreal Engine 5.3** e **Nvidia Sionna**. Il software sviluppato consente di modellare, calcolare e visualizzare la copertura del segnale in uno scenario urbano complesso.

### Tecnologie utilizzate
- **Unreal Engine 5.3**: Motore grafico per la simulazione 3D in tempo reale.
- **Blender 4.1**: Utilizzato per la creazione dei modelli 3D degli edifici urbani.
- **Nvidia Sionna**: Libreria per la simulazione della propagazione del segnale wireless.
- **Python & TensorFlow**: Linguaggi e librerie per l'automazione e l'analisi dei dati della simulazione.

## Obiettivi

L'obiettivo del progetto è fornire uno strumento che:
1. Simuli con precisione la propagazione del segnale in un ambiente urbano complesso.
2. Visualizzi i percorsi del segnale (paths) e le mappe di copertura (coverage maps) attraverso un digital twin realistico.
3. Consenta il confronto tra i dati simulati e quelli reali per validare l'accuratezza del modello.

## Funzionalità principali

1. **Creazione del modello 3D**: Utilizzando **Blender** e i dati di **OpenStreetMap**, viene generato un modello 3D dell'area urbana.
2. **Simulazione della propagazione del segnale**: Grazie a **Nvidia Sionna** e al **ray tracing differenziabile**, viene simulata la propagazione del segnale tra trasmettitori (TX) e ricevitori (RX).
3. **Visualizzazione del percorso del segnale**: In **Unreal Engine**, i percorsi del segnale vengono tracciati e visualizzati tramite `Blueprints` che disegnano linee di debug tra TX e RX.
4. **Generazione di mappe di copertura**: Viene generata una mappa di copertura (coverage map) ad alta risoluzione, che rappresenta la potenza del segnale in decibel per ogni punto dell'area urbana.

## Struttura del progetto

Il progetto è suddiviso in quattro fasi principali:
1. **Importazione del modello urbano**: I dati geografici vengono importati da OpenStreetMap e convertiti in modelli 3D utilizzando Blender.
2. **Simulazione della propagazione**: Viene utilizzato Nvidia Sionna per calcolare i percorsi del segnale e generare la mappa di copertura.
3. **Visualizzazione**: I risultati della simulazione vengono importati in Unreal Engine per la visualizzazione interattiva.
4. **Validazione del modello**: I risultati della simulazione vengono confrontati con dati reali raccolti sul campo per validare il modello.

## Come eseguire il progetto

### Prerequisiti
- **Unreal Engine 5.3**
- **Blender 4.1**
- **Nvidia Sionna**
- **Python 3.8+** con **TensorFlow**

### Istruzioni

1. **Importazione dei dati**:
   - Aprire **Blender** e utilizzare l'add-on `Blosm` per importare i dati da **OpenStreetMap**.
   - Esportare il modello 3D come file `.obj` e `.xml` per Unreal Engine e Nvidia Sionna rispettivamente.

2. **Simulazione**:
   - Eseguire lo script Python per avviare Nvidia Sionna e calcolare i percorsi del segnale e la mappa di copertura.
   - Esportare i risultati in formato CSV e immagine.

3. **Visualizzazione**:
   - Importare i dati esportati in **Unreal Engine**.
   - Utilizzare i `Blueprints` forniti per visualizzare i percorsi del segnale e la mappa di copertura.

## Risultati

Il progetto ha permesso di creare un digital twin dettagliato di un ambiente urbano, calcolando percorsi di segnale complessi e generando una mappa di copertura ad alta risoluzione. I risultati sono stati confrontati con dati reali per verificarne la precisione.

## Futuri sviluppi

- Miglioramento del modello per includere ostacoli dinamici (ad esempio, veicoli e persone).
- Integrazione con modelli di machine learning per l'ottimizzazione della rete in tempo reale.

## Autori

- **Carlo Zamuner** - Laureando in Ingegneria Informatica, delle Comunicazioni ed Elettronica presso l'Università di Trento.
