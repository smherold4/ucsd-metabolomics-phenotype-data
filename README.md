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
INSERT INTO cohort (name, method) VALUES ('FINRISK', 'LCMS_BAL');
INSERT INTO cohort (name, method) VALUES ('FHS', 'LCMS_BAL');
```

### Importing raw cohort measurements by plate_well
```
python main_sql.py \
  --mode raw_ingestion \
  --cohort-name FINRISK \
  --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/finrisk/ProcessedDataRawDeadducted.csv \
  --units raw \
  --verbose
```

```
python main_sql.py  \
  --mode raw_ingestion  \
  --cohort-name FHS \
  --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/FHS/ProcessedDataRawDeadducted.csv \
  --units raw  \
  --verbose
```

### Mapping Keys (Subjects, Samples, Sample Barcodes, Plate Wells)

```
python main_sql.py \
  --mode sample_key_ingestion  \
  --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv \
  --cohort-name FINRISK \
  --verbose
```

### Indexing Subjects in Elasticsearch
#### (this step will read the 'Age At Sample Collection' from the phenotype data and save it to the subject)

```
python main_es.py \
  --index subjects \
  --action populate \
  --cohort-name FINRISK \
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
  --cohort-name FINRISK \
  --alignment-cohort-name FHS \
  --alignment-file /volume1/Database/Framingham/metabolomics/LCMS_EIC/AlignedPeaksWithFin.csv \
  --alignment-cohort-col A \
  --verbose
```
