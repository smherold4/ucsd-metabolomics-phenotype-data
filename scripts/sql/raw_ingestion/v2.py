import csv
from models import *
from db import db_connection
import pandas as pd
import re

CSV_CHUNKSIZE = 8000
COLUMN_OF_FIRST_MEASUREMENT = 14

# Customize this by cohort
SAMP_ID_REGEX = r'SampID\_+([A-Za-z0-9\-]+)$'


def find_or_create_cohort_compound(session, series, cohort, calculate_median):
    local_compound_id = series['local_Lab']
    if pd.isnull(local_compound_id):
        return None
    mz = series['MZ']
    rt = series['RT']
    cross_variation = series['CV']
    ml_score = series['ML_Score']
    cohort_compound = session.query(CohortCompound).filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.local_compound_id == str(local_compound_id),
    ).first() or CohortCompound(
        cohort, local_compound_id, mz, rt, cross_variation, ml_score
    )
    if calculate_median:
        cohort_compound.median_measurement = series[COLUMN_OF_FIRST_MEASUREMENT:].median()
    session.add(cohort_compound)
    session.commit()
    return cohort_compound


def extract_cohort_sample_id(string):
    re_match = re.search(SAMP_ID_REGEX, string)
    if re_match:
        return re_match.group(1)


def find_or_create_sample(session, cohort, cohort_sample_id):
    sample = session.query(Sample).filter(
        Sample.cohort == cohort,
        Sample.cohort_sample_id == cohort_sample_id,
    ).first() or Sample(cohort.id, None, cohort_sample_id, None, None)
    if not sample.id:
        session.add(sample)
        session.commit()
    return sample


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
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    Measurement = measurement_class_factory(cohort)

    assert args.units in Dataset.UNITS, 'Invalid units provided. Must be one of: {}'.format(Dataset.UNITS)
    dataset = find_or_create_dataset(cohort, args.units, session)
    sample_ids_cache = {}
    row_count = 0
    for df in pd.read_csv(args.file, chunksize=(args.csv_chunksize or CSV_CHUNKSIZE)):
        sample_id_labels = df.columns[COLUMN_OF_FIRST_MEASUREMENT:]
        for _, row in df.iterrows():
            sql = "INSERT INTO {} (sample_id, cohort_compound_id, dataset_id, measurement) VALUES ".format(Measurement.__tablename__)
            values = []
            row_count += 1
            cohort_compound = find_or_create_cohort_compound(session, row, cohort, args.units == 'raw')
            if not cohort_compound:
                continue
            for sample_id_label in sample_id_labels:
                cohort_sample_id = extract_cohort_sample_id(sample_id_label)
                if not cohort_sample_id:
                    continue
                if args.exam_no:
                    cohort_sample_id = cohort_sample_id + "-" + args.exam_no
                sample_id = sample_ids_cache.get(cohort_sample_id) or find_or_create_sample(session, cohort, cohort_sample_id).id
                sample_ids_cache[cohort_sample_id] = sample_id

                if not pd.isnull(row[sample_id_label]):
                    values.append("({}, {}, {}, {})".format(sample_id, cohort_compound.id, dataset.id, row[sample_id_label]))
            if args.verbose:
                print "Inserting {} records into {} for metabolite {}.  Row count is {}".format(len(values), Measurement.__tablename__, cohort_compound.local_compound_id, row_count)
            if len(values):
                sql += ",".join(values)
                session.execute(sql)
                session.commit()
