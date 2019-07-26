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
INSERT INTO cohort (name, method) VALUES ('Finrisk', 'LCMS');
INSERT INTO cohort (name, method) VALUES ('FHS', 'LCMS');
```

### Importing descriptions
```
python main_sql.py \
  --cohort-name 'Finrisk' \
  --mode 'description_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.description.csv \
  --units normalized
```

### Mapping Keys (Subjects, Samples, Sample Barcodes, Plate Wells)

```
python main_sql.py --mode sample_key_ingestion  --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv --cohort-name Finrisk --verbose
```

### Importing measurements

```
python main_sql.py \
  --cohort-name 'Finrisk' \
  --mode 'measurements_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.csv \
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
  --subject-id-label PLASMA_ID
  --verbose
```

```
python main_es.py \
  --index subjects \
  --action populate \
  --cohort-name FHS \
  --file /volume1/Database/Framingham/phenotype/pheno_data_fhs_20171210_TL.csv \
  --subject-id-label SubjectID \
  --verbose
```
