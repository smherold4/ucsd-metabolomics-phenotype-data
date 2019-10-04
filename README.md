# Metabolomics SQL and Elasticsearch Scripts

### STEP 0: Python setup
```
$ pip install -r requirements.txt

(if on Linux server)
$ pip install -r requirements-linux.txt
```

### STEP 1: Add new cohort directly to SQL database
```
INSERT INTO cohort (name, source) VALUES ('FINRISK', 'plasma');
```

### STEP 2: Create a new measurement table for the new cohort in the SQL database
- ##### FOR TABLE NAME - ALL LOWERCASE, SPACES AND DASHES SHOULD BECOME UNDERSCORES, SEE METHOD `get_tablename()`
```
CREATE TABLE ciao_sage_measurement (
    id SERIAL PRIMARY KEY,
    sample_id integer NOT NULL,
    cohort_compound_id integer NOT NULL,
    dataset_id integer NOT NULL,
    measurement numeric(80,30) NOT NULL
);
```

### STEP 3: Metabolite Measurement Ingestion - Import Metabolite Measurements And Create Samples In SQL
- ##### PRIOR TO THIS STEP YOU MUST CUSTOMIZE THE `SAMP_ID_REGEX` and/or `PLATE_WELL_REGEX` IN THE CODE
- ##### SET THE `UNIQ_LOOKUP_VALUE` to use either `cohort_sample_id` or `plate_well`.  If both `cohort_sample_id` and `plate_well` can be extracted from the labels, then `cohort_sample_id` is probably the preferred lookup value.

- ##### THIS STEP SHOULD BE RUN ONCE FOR 'RAW_RELABELLED.CSV' AND ONCE FOR 'NORMALIZEDV2_RELABELLED.CSV'


```
python main_sql.py --mode measurement_ingestion --cohort-name FINRISK --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/finrisk/ProcessedDataRawDeadducted.csv --units raw --method LCMS_BAL --col-of-first-measurement O
```


```
python main_sql.py --mode measurement_ingestion --cohort-name FHS --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/FHS/ProcessedDataRawDeadducted.csv --units raw --method LCMS_BAL --col-of-first-measurement O
```


```
python main_sql.py --mode measurement_ingestion --cohort-name MESA --exam-no 2 --units raw --method LCMS_BAL --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA02/ProcessedDataRawDeadducted_relabelled.csv --col-of-first-measurement O
```


```
python main_sql.py --mode measurement_ingestion --cohort-name MESA --exam-no 4 --units raw --method LCMS_BAL --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA04/ProcessedDataRawDeadducted_relabelled.csv --col-of-first-measurement O
```


```
python main_sql.py --mode measurement_ingestion --cohort-name 'VITAL CTSC' --units raw --method LCMS_BAL --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/VITAL\ CTSC/ProcessedDataRawDeadducted_relabelled.csv --col-of-first-measurement O
```

```
python main_sql.py --mode measurement_ingestion --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/FinTwin/ProcessedDataNormDeadductedV2.csv  --cohort-name FinTwin --units normalized --method LCMS_BAL --col-of-first-measurement K
```

### STEP 4: Key Ingestion - Mapping Samples to Plate_Well and Creating Subjects For Each Sample
- ##### PRIOR TO THIS STEP YOU MUST CONFIRM THAT THE COLUMNS IN THE CSV AGREE WITH THE `KEY_COLUMNS` CONSTANT


```
python main_sql.py --mode key_mapping --file /volume1/Database/FINRISK2002/metabolomics/FINRISK_Example_Key.csv --cohort-name FINRISK
```


```
python main_sql.py --mode key_mapping --file /volume1/Database/Framingham/metabolomics/FHS_Patient_Keys.csv --cohort-name FHS
```


```
python main_sql.py --mode key_mapping --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/MESA04/SampleKey.csv --cohort-name MESA --exam-no 4
```


```
python main_sql.py --mode key_mapping --file /volume1/Jain\ Lab\ Data/MassSpecDatabase/Eicosanoid\ method/VITAL\ CTSC/SampleKey.csv --cohort-name 'VITAL CTSC'
```

### STEP 5: Elasticsearch Indexing - metabolite_samples

```
python main_es.py --index metabolite_samples --action populate --cohort-name FINRISK
```

```
python main_es.py --index metabolite_samples --action populate --cohort-name FHS
```

### STEP 6: Elasticsearch Indexing - metabolite_alignments
- ##### This script looks in the '/volume1/Jain Lab Data/MassSpecDatabase/Eicosanoid method/' for alignment files


```
python main_es.py --index metabolite_alignments --action populate --cohort-name FINRISK
```


```
python main_es.py --index metabolite_alignments --action populate --cohort-name FHS
```

### STEP 7.A: Elasticsearch Indexing - subject_phenotypes



```
python main_es.py --index subject_phenotypes --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/phenotype/FINRISK2002/F2015_60_Salomaa_Jain_dataFR02_FU16_2018-11-16_FR02_TL.csv  --subject-id-label PLASMA_ID
```


```
python main_es.py --index subject_phenotypes --action populate --cohort-name FHS --phenotype-file /volume1/Database/phenotype/FHS/pheno_data_fhs_20171210_TL.csv --subject-id-label SubjectID
```

```
python main_es.py --index subject_phenotypes --action populate --cohort-name 'VITAL 400' --phenotype-file /volume1/Database/phenotype/VITAL400/vital_20180801.csv --subject-id-label subject_ID
```

### STEP 7.B: Elasticsearch Indexing - sample_phenotypes


```
python main_es.py --action populate --index sample_phenotypes --phenotype-file /volume1/Database/phenotype/MESA/MESA2_20160520.csv --cohort-name MESA --exam-no 2 --subject-id-label idno
```

### STEP 8: Elasticsearch Indexing - phenotype_descriptions
- ##### THIS MUST BE DONE LAST SO THAT WE CAN INFER THE DATATYPE


```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FINRISK --phenotype-file /volume1/Database/phenotype/FINRISK2002/FR02_pheno_annotations.csv
```


```
python main_es.py --index phenotype_descriptions --action populate --cohort-name FHS --phenotype-file /volume1/Database/phenotype/FHS/pheno_data_fhs_description_KM.csv
```

## MICROBIOME INDEXING

#### `microbiome_abundances`
```
python main_es.py --index microbiome_abundances --action populate --cohort-name AGP --microbiome-file /volume1/Database/microbiome/agp/microbiome_abundance.txt
```

#### `microbiome_alignments`
```
python main_es.py --index microbiome_alignments --action populate --cohort-name FINRISK --microbiome-file /volume1/Database/microbiome/finrisk/microbiome_alignments.txt
```

```
python main_es.py --index microbiome_alignments --action populate --cohort-name GGMP --microbiome-file /volume1/Database/microbiome/ggmp/microbiome_alignments.txt
```

#### `microbiome_sequenes`
```
python main_es.py --index microbiome_sequences --action populate --cohort-name FINRISK --microbiome-file /volume1/Database/microbiome/finrisk/microbiome_sequence.txt
```

```
python main_es.py --index microbiome_sequences --action populate --cohort-name AGP --microbiome-file /volume1/Database/microbiome/agp/microbiome_sequence.txt
```
