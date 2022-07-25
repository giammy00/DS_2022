Consumi Elettrici del Trentino
==============================

Progetto sull'analisi dati dei consumi elettrici della provincia di Trento e del comune di Trento.
Relativo all'esame del corso "Introduzione alla Data Science per fisici" dell'Università di Trento.

## Riproduzione dei risultati

Clonare la repository ed eseguire i seguenti comandi su terminale bash. È necessario aver installato conda.

1. Per creare un ambiente conda con i pacchetti necessari eseguire il comando <br>
	`make requirements` <br>
   Questo crea un ambiente chiamato `DS_2022`. Attivarlo con <br>
   	`conda activate DS_2022` <br>
   	
2. Eseguire `make data` per generare diversi file nel formato .pkl che contengono diversi dataframe 
    contenenti dati di meteo, consumi e inquinamento, separati. Vengono salvati nella cartella data/interim.
   Una volta creati, essi possono essere velocemente importati eseguendo
   	`from trentodatalib import meteo, consumi, inquinamento` nello script python dove si vogliono usare.

2. Poi si possono creare i dataset per la classificazione e per la regressione eseguendo <br>
	`make features` <br>
   Questo crea i dataset desiderati e pronti per il training nella cartella data/processed, sempre nel formato .pkl
   
3. Una volta creati tutti i dataset la visualizzazione dei risultati, in un notebook o in una console iPython, si possono importare i moduli contenuti in src/visualization ed eseguire le funzioni che sono contenute in essi. In particolare:
	+ EDA_Trento.py contiene due funzioni che plottano analisi dei consumi nelle due zone in cui è suddiviso trento
	+ EDA_Provincia.py
	+ mappe.py contiene varie funzioni che plottano mappe
	+ classificazione.py contiene funzioni per plot delle matrici di confusione dei classificatori
	+ plotregression.py esegue regressione lineare diverse volte variando il numero di features e visualizza i risultati.

4. Per allenare i modelli relativi a classificazione e regressione eseguire <br>
	`make train` <br>
   I modelli ricavati in questo training vengono esportati nel formato .joblib nella cartella ./models

## Repo structure
```
.
├── data
│   ├── external 
│   │   ├── APPA_inquinamento_aria_Nov_Dec_2013.csv
│   │   ├── Com01012013_WGS84.cpg
│   │   ├── Com01012013_WGS84.dbf
│   │   ├── Com01012013_WGS84.prj
│   │   ├── Com01012013_WGS84.shp
│   │   └── Com01012013_WGS84.shx
│   ├── interim
│   ├── processed
│   └── raw
│       ├── line.csv
│       ├── meteotrentino-weather-station-data.json
│       ├── SET-dec-2013.csv
│       ├── SET-nov-2013.csv
│       └── trentino-grid.geojson
├── DS_2022.yml  <-- conda image to reproduce result
├── LICENSE
├── Makefile
├── models
├── notebooks
│   ├── PresentazioneEDA.ipynb
│   ├── PresentazioneEDA.slides.html
├── requirements.txt
├── setup.py
├── src
│   ├── build_features_classification.py
│   ├── build_features_regression.py
│   ├── data
│   │   ├── make_dataset_consumi.py
│   │   ├── make_dataset_inquinamento.py
│   │   ├── make_dataset_meteo.py
│   │   └── make_raw_data.py
│   ├── models
│   │   ├── predict_Model_Regression.py
│   │   ├── train_model_classification.py
│   │   └── train_model_regression.py
│   ├── plotmappastazioni.py
│   ├── trentodatalib
│   │   ├── consumi.py
│   │   ├── funzioni.py
│   │   ├── __init__.py
│   │   ├── inquinamento.py
│   │   ├── meteo.py
│   │   ├── rawdatabase.py
│   │   ├── readme.txt
│   │   └── trentopaths.py
│   └── visualization
│       ├── classificazione.py
│       ├── EDA_provincia.py
│       ├── EDA_Trento.py
│       ├── __init__.py
│       ├── mappe.py
│       └── plotregression.py
└── test_environment.py
```



<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
