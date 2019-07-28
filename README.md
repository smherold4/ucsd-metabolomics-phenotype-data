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
INSERT INTO cohort (name, method) VALUES ('Finrisk', 'LCMS_BAL');
INSERT INTO cohort (name, method) VALUES ('FHS', 'LCMS_BAL');
```

### Importing descriptions
```
python main_sql.py \
  --cohort-name 'Finrisk' \
  --mode 'description_ingestion' \
  --file /volume1/Database/FINRISK2002/metabolomics/LCMS_EIC/FR_ml_mad_norm.description.csv \
```

### Mapping Keys (Subjects, Samples, Sample Barcodes, Plate Wells)

```
python main_sql.py \
  --mode sample_key_ingestion  \
  --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv \
  --cohort-name Finrisk \
  --verbose
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
#### (this step will read the 'Age At Sample Collection' from the phenotype data and save it to the subject)

```
python main_es.py \
  --index subjects \
  --action populate \
  --cohort-name Finrisk \
  --file /volume1/Database/FINRISK2002/phenotype/F2015_60_Salomaa_Jain_dataFR02_FU16_2018-11-16_FR02_TL.csv \
  --subject-id-label PLASMA_ID \
  --age-at-sample-collection-label BL_AGE \
  --verbose
```

```
python main_es.py \
  --index subjects \
  --action populate \
  --cohort-name FHS \
  --file /volume1/Database/Framingham/phenotype/pheno_data_fhs_20171210_TL.csv \
  --subject-id-label SubjectID \
  --age-at-sample-collection-label BL_AGE \
  --verbose
```

### Indexing Metabolomics in Elasticsearch

```
python main_es.py \
  --index metabolomics \
  --action populate \
  --cohort-name Finrisk \
  --alignment-cohort-name FHS \
  --alignment-file /volume1/Database/Framingham/metabolomics/LCMS_EIC/AlignedPeaksWithFin.csv \
  --alignment-cohort-col A \
  --verbose
```
