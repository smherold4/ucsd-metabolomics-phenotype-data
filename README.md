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

### Mapping Keys (Sample Barcodes, Plate Wells, SubjectID, etc)

```
python main_sql.py \
  --mode sample_key_ingestion  \
  --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv \
  --cohort-name FINRISK \
  --verbose
```

```
python main_sql.py \
  --mode sample_key_ingestion  \
  --file /volume1/Database/Framingham/metabolomics/FHS_Patient_Keys.csv \
  --cohort-name FHS \
  --verbose
```

### Elasticsearch Indexing metabolite_samples

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FINRISK --index-batch-size 200000
```

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FHS --index-batch-size 200000
```

### Elasticsearch Indexing metabolite_alignments

