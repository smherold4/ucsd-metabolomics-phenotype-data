# UCSD Metabolomics SQL storage
Metabolomics and Phenotype ElasticSearch project

### Python setup
```
$ pip install -r requirements.txt
```
OR (if on Synology server)
```
pip install -r requirements-synology.txt
```

### Viewing Help File
```
python main.py -h
```

### Adding new study names
```
INSERT INTO cohort (name) VALUES ('Finrisk');
INSERT INTO cohort (name) VALUES ('FHS');
```

### Importing descriptions
```
python main_sql.py \
  --cohort-name 'Finrisk' \
  --mode 'description_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.description.csv \
  --method LCMS \
  --units normalized
```

### Importing measurements

```
python main_sql.py \
  --cohort-name 'Finrisk' \
  --mode 'measurements_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.csv \
  --method LCMS \
  --units normalized \
  --verbose
```

### Indexing Subjects in Elasticsearch

```
python main_es.py \
  --index subjects \
  --action populate \
  --cohort-name Finrisk \
  --file /volume1/Database/FINRISK2002/phenotype/F2015_60_Salomaa_Jain_dataFR02_FU16_2018-11-16_FR02_TL.csv \
  --verbose
```
