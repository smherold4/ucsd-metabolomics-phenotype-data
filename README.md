# UCSD Metabolomics SQL storage
Metabolomics and Phenotype ElasticSearch project

### Python setup
```
$ pip install -r requirements.txt
```

### Viewing Help File
```
python main.py -h
```

### Adding new study names
```
INSERT INTO study (name) VALUES ('Finrisk');
INSERT INTO study (name) VALUES ('FHS');
```

### Importing descriptions without alignment
```
python main.py \
  --study-name 'Finrisk' \
  --mode 'description_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.description.csv \
  --method LCMS \
  --units normalized \
  --skip-alignment
```

### Importing descriptions with alignment
```
python main.py \
  --study-name 'FHS' \
  --mode 'description_ingestion' \
  --file ~/Desktop/FHS_ml_mad_norm.description.csv \
  --method 'LCMS' \
  --units normalized \
  --alignment-file ~/Desktop/AlignedPeaksWithFin.csv \
  --alignment-cohort-study 'Finrisk' \
  --alignment-cohort-column B
```

### Importing measurements

```
python main.py \
  --study-name 'Finrisk' \
  --mode 'measurements_ingestion' \
  --file ~/Desktop/FR_ml_mad_norm.csv \
  --method LCMS \
  --units normalized \
  --verbose
```
