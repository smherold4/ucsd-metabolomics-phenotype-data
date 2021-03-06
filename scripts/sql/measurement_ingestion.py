import csv
from models import *
from db import db_connection
import pandas as pd
import re
import string

CSV_CHUNKSIZE = 8000

# Customize this by cohort
SAMP_ID_REGEX = r'^(a[0-9]+)_500FG'
PLATE_WELL_REGEX = r'Plate_([0-9]{2}\_[0-9]{2})\_'


def find_or_create_cohort_compound(session, series, cohort, method, calc_agg_stats, col_of_first_measurement):
    local_compound_id = series['local_Lab']
    if pd.isnull(local_compound_id):
        return None
    mz = series['MZ']
    rt = series['RT']
    cross_variation = series['CV']
    ml_score = series['ML_Score']
    cohort_compound = session.query(CohortCompound).filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.method == method,
        CohortCompound.local_compound_id == str(local_compound_id),
    ).first() or CohortCompound(
        cohort, method, local_compound_id, mz, rt, cross_variation, ml_score
    )
    if calc_agg_stats:
        measurements = series[col_of_first_measurement:]
        cohort_compound.median_measurement = measurements.median()
        cohort_compound.prevalence = 100.0 * sum(1 for m in measurements if not pd.isnull(m)) / len(measurements)
        cohort_compound.min_raw = measurements.min()
        cohort_compound.max_raw = measurements.max()
    session.add(cohort_compound)
    session.commit()
    return cohort_compound


def extract_cohort_sample_id(string):
    re_match = re.search(SAMP_ID_REGEX, string)
    if re_match:
        return re_match.group(1)

def extract_plate_well(string):
    re_match = re.search(PLATE_WELL_REGEX, string)
    if re_match:
        return re_match.group(1)

def find_or_create_sample(session, cohort, cohort_sample_id, plate_well):
    sample = find_sample(session, cohort, cohort_sample_id, plate_well) or Sample(cohort.id, None, cohort_sample_id, None, plate_well)
    if not sample.id:
        session.add(sample)
        session.commit()
    return sample

def find_sample(session, cohort, cohort_sample_id, plate_well):
    if not pd.isnull(cohort_sample_id):
        return session.query(Sample).filter(
            Sample.cohort == cohort,
            Sample.cohort_sample_id == cohort_sample_id,
        ).first()
    elif not pd.isnull(plate_well):
        return session.query(Sample).filter(
            Sample.cohort == cohort,
            Sample.plate_well == plate_well,
        ).first()

def find_or_create_dataset(cohort, units, session):
    dataset = session.query(Dataset).filter(
        Dataset.cohort == cohort,
        Dataset.units == units,
    ).first()
    if dataset:
        return dataset
    dataset = Dataset(cohort, units)
    session.add(dataset)
    session.commit()
    return dataset


def run(args):
    assert str(args.col_of_first_measurement) in string.ascii_uppercase, "Must provide --col-of-first-measurement between A and Z"
    col_of_first_measurement = string.ascii_uppercase.index(args.col_of_first_measurement)
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    Measurement = measurement_class_factory(cohort)

    assert args.units in Dataset.UNITS, 'Invalid units provided. Must be one of: {}'.format(Dataset.UNITS)
    assert args.method in CohortCompound.METHODS, 'Invalid method provided. Must be one of: {}'.format(CohortCompound.METHODS)
    dataset = find_or_create_dataset(cohort, args.units, session)
    sample_ids_cache = {}
    row_count = 0
    for df in pd.read_csv(args.file, chunksize=(args.csv_chunksize or CSV_CHUNKSIZE)):
        sample_id_labels = df.columns[col_of_first_measurement:]
        for _, row in df.iterrows():
            sql = "INSERT INTO {} (sample_id, cohort_compound_id, dataset_id, measurement) VALUES ".format(Measurement.__tablename__)
            values = []
            row_count += 1
            cohort_compound = find_or_create_cohort_compound(session, row, cohort, args.method, args.units == 'raw', col_of_first_measurement)
            if not cohort_compound:
                continue
            for sample_id_label in sample_id_labels:
                cohort_sample_id = extract_cohort_sample_id(sample_id_label)
                plate_well = extract_plate_well(sample_id_label)

                # HERE YOU CHOOSE WHICH FIELD (cohort_sample_id or plate_well) TO DO THE UNIQUE LOOKUP ON
                UNIQ_LOOKUP_VALUE = plate_well

                if pd.isnull(UNIQ_LOOKUP_VALUE):
                    continue
                sample_id = sample_ids_cache.get(UNIQ_LOOKUP_VALUE) or find_or_create_sample(session, cohort, cohort_sample_id, plate_well).id
                sample_ids_cache[UNIQ_LOOKUP_VALUE] = sample_id

                values.append("({}, {}, {}, {})".format(sample_id, cohort_compound.id, dataset.id, row[sample_id_label]))
            print "Inserting {} records into {} for metabolite {}.  Row count is {}".format(
                len(values), Measurement.__tablename__, cohort_compound.local_compound_id, row_count)
            if len(values):
                sql += ",".join(values)
                session.execute(sql)
                session.commit()
