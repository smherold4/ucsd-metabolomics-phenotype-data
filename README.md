# UCSD Metabolomics SQL storage
Metabolomics and Phenotype ElasticSearch project

### Python setup
```
$ pip install -r requirements.txt

(if on Linux server)
$ pip install -r requirements-linux.txt
```

### Add cohorts directly to SQL database
```
INSERT INTO cohort (name, method) VALUES ('FINRISK', 'LCMS_BAL');
INSERT INTO cohort (name, method) VALUES ('FHS', 'LCMS_BAL');
```

### Importing Raw Files

FINRISK
```
python main_sql.py --mode raw_ingestion --cohort-name FINRISK --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/finrisk/ProcessedDataRawDeadducted.csv --units raw --verbose
```

FHS
```
python main_sql.py --mode raw_ingestion --cohort-name FHS --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/FHS/ProcessedDataRawDeadducted.csv --units raw --verbose
```

MESA
```
python main_sql.py --mode raw_ingestion --cohort-name MESA --units raw --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA/ProcessedDataRawDeadducted_relabelled.csv --verbose
```

### Mapping Keys (Sample Barcodes, Plate Wells, SubjectID, etc)

```
python main_sql.py --mode sample_key_ingestion --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv --cohort-name FINRISK --verbose
```

```
python main_sql.py --mode sample_key_ingestion --file /volume1/Database/Framingham/metabolomics/FHS_Patient_Keys.csv --cohort-name FHS --verbose
```

### Elasticsearch Indexing metabolite_samples

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FINRISK --index-batch-size 200000
```

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FHS --index-batch-size 200000
```

### Elasticsearch Indexing metabolite_alignments

```
python main_es.py --index metabolite_alignments --action populate --cohort-name FINRISK --verbose
```

```
python main_es.py --index metabolite_alignments --action populate --cohort-name FHS --verbose
```

### Elasticsearch Indexing subject_phenotypes

```
python main_es.py --index subject_phenotypes --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/FINRISK2002/phenotype/F2015_60_Salomaa_Jain_dataFR02_FU16_2018-11-16_FR02_TL.csv --subject-id-label PLASMA_ID --verbose
```

```
python main_es.py --index subject_phenotypes --action populate --cohort-name FHS --phenotype-file /volume1/Database/Framingham/phenotype/pheno_data_fhs_20171210_TL.csv --subject-id-label SubjectID --verbose
```

### Elasticsearch Indexing phenotype_descriptions
```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/phenotype/FINRISK2002/FR02_pheno_annotations.csv --verbose
```

```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FHS --phenotype-file /volume1/Database/phenotype/FHS/pheno_data_fhs_description_KM.csv --verbose
```
