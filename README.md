# Metabolomics SQL and Elasticsearch Scripts

### STEP 0: Python setup
```
$ pip install -r requirements.txt

(if on Linux server)
$ pip install -r requirements-linux.txt
```

### STEP 1: Add new cohort directly to SQL database
```
INSERT INTO cohort (name, method) VALUES ('CIAO-SAGE', 'LCMS_BAL');
```

### STEP 2: Create a new measurement table for the new cohort in the SQL database
- ##### SPACES AND DASHES SHOULD BECOME UNDERSCORES
- ##### ALL LOWERCASE
```
CREATE TABLE ciao_sage_measurement (
    id SERIAL PRIMARY KEY,
    sample_id integer NOT NULL,
    cohort_compound_id integer NOT NULL,
    dataset_id integer NOT NULL,
    measurement numeric(80,30) NOT NULL
);
```

### STEP 3: Raw Ingestion - Import Metabolite Measurements And Create Samples In SQL
- ##### PRIOR TO THIS STEP YOU MUST CUSTOMIZE THE `SAMP_ID_REGEX` IN THE CODE, AND ENSURE THAT `COLUMN_OF_FIRST_MEASUREMENT` IS CORRECT FOR THE INGESTION FILE
- ##### THIS STEP SHOULD BE RUN ONCE FOR 'RAW_RELABELLED.CSV' AND ONCE FOR 'NORMALIZEDV2_RELABELLED.CSV'


```
python main_sql.py --mode raw_ingestion --cohort-name FINRISK --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/finrisk/ProcessedDataRawDeadducted.csv --units raw --verbose
```


```
python main_sql.py --mode raw_ingestion --cohort-name FHS --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/FHS/ProcessedDataRawDeadducted.csv --units raw --verbose
```


```
python main_sql.py --mode raw_ingestion --cohort-name MESA --exam-no 2 --units raw --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA02/ProcessedDataRawDeadducted_relabelled.csv --verbose
```


```
python main_sql.py --mode raw_ingestion --cohort-name MESA --exam-no 4 --units raw --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA04/ProcessedDataRawDeadducted_relabelled.csv --verbose
```


```
python main_sql.py --mode raw_ingestion --cohort-name 'VITAL CTSC' --units raw --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/VITAL\ CTSC/ProcessedDataRawDeadducted_relabelled.csv --verbose
```

### STEP 4: Key Ingestion - Mapping Samples to Plate_Well and Creating Subjects For Each Sample
- ##### PRIOR TO THIS STEP YOU MUST CUSTOMIZE THE `SUBJECT_ID_REGEX` IN THE CODE


```
python main_sql.py --mode key_ingestion --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv --cohort-name FINRISK --verbose
```


```
python main_sql.py --mode key_ingestion --file /volume1/Database/Framingham/metabolomics/FHS_Patient_Keys.csv --cohort-name FHS --verbose
```


```
python main_sql.py --mode key_ingestion --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA04/SampleKey.csv --cohort-name MESA --exam-no 4 --verbose
```


```
python main_sql.py --mode key_ingestion --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/VITAL\ CTSC/SampleKey.csv --cohort-name 'VITAL CTSC' --verbose
```

### STEP 5: Elasticsearch Indexing `metabolite_samples`

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FINRISK
```

```
python main_es.py --index metabolite_samples --action populate --verbose --cohort-name FHS
```

### STEP 6: Elasticsearch Indexing metabolite_alignments
- ##### PRIOR TO THIS STEP YOU MUST ADD A FILE UNDER THE ALIGNMENT FILE PARAMS WITH THE NAME OF THE COHORT
- ##### FOR FILE NAME - IT IS CASE SENSITIVE AND SPACES AND DASHES SHOULD WRITTEN AS UNDERSCORES
- ##### THIS FILE WILL LIST ALL THE ALIGNMENT FILES ON THE NAS SERVER


```
python main_es.py --index metabolite_alignments --action populate --cohort-name FINRISK --verbose
```


```
python main_es.py --index metabolite_alignments --action populate --cohort-name FHS --verbose
```

### STEP 7.A: Elasticsearch Indexing subject_phenotypes



```
python main_es.py --index subject_phenotypes --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/phenotype/FINRISK2002/F2015_60_Salomaa_Jain_dataFR02_FU16_2018-11-16_FR02_TL.csv  --subject-id-label PLASMA_ID --verbose
```


```
python main_es.py --index subject_phenotypes --action populate --cohort-name FHS --phenotype-file /volume1/Database/phenotype/FHS/pheno_data_fhs_20171210_TL.csv --subject-id-label SubjectID --verbose
```

### STEP 7.B: Elasticsearch Indexing sample_phenotypes


```
python main_es.py --action populate --index sample_phenotypes --phenotype-file /volume1/Database/phenotype/MESA/MESA2_20160520.csv --cohort-name MESA --exam-no 2 --subject-id-label idno --verbose
```

### STEP 8: Elasticsearch Indexing phenotype_descriptions
- ##### THIS MUST BE DONE AFTER STEP 6 SO THAT WE CAN INFER THE DATATYPE


```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/phenotype/FINRISK2002/FR02_pheno_annotations.csv --verbose
```


```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FHS --phenotype-file /volume1/Database/phenotype/FHS/pheno_data_fhs_description_KM.csv --verbose
```
