# This version of the script is for fhs and finrisk before the columns were relabelled from plate_well to having cohort_sampe_id

import csv
from models import *
from db import db_connection
import pandas as pd
import re

CSV_CHUNKSIZE = 8000
COLUMN_OF_FIRST_MEASUREMENT = 14
PLATE_WELL_REGEX = r'\_Plate\_(\d+\_\d+)\_'


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


def extract_plate_well(string):
    re_match = re.search(PLATE_WELL_REGEX, string)
    if re_match:
        return re_match.group(1)


# def find_or_create_subject(session, cohort, local_subject_id):
#     subject = session.query(Subject).filter(
#         Subject.cohort == cohort,
#         Subject.local_subject_id == local_subject_id
#     ).first() or Subject(cohort, local_subject_id)
#     if not subject.id:
#         session.add(subject)
#         session.commit()
#     return subject


def find_or_create_sample(session, cohort, plate_well):
    sample = session.query(Sample).filter(
        Sample.cohort == cohort,
        Sample.plate_well == plate_well,
    ).first() or Sample(cohort.id, None, None, None, plate_well)
    if not sample.id:
        session.add(sample)
        session.commit()
    return sample


def run(args):
    if args.measurement_tablename:
        Measurement.__tablename = args.measurement_tablename
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(
        args.cohort_name)
    assert args.units in Dataset.UNITS, 'Invalid units provided. Must be one of: {}'.format(Dataset.UNITS)
    dataset = Dataset(cohort, args.units)
    session.add(dataset)
    session.commit()
    sample_ids_cache = {}
    row_count = 0
    for df in pd.read_csv(args.file, chunksize=(args.csv_chunksize or CSV_CHUNKSIZE)):
        sample_id_labels = df.columns[COLUMN_OF_FIRST_MEASUREMENT:]
        for _, row in df.iterrows():
            sql = "INSERT INTO measurement (sample_id, cohort_compound_id, dataset_id, measurement) VALUES "
            values = []
            row_count += 1
            cohort_compound = find_or_create_cohort_compound(session, row, cohort, args.units == 'raw')
            if not cohort_compound:
                continue
            for sample_id_label in sample_id_labels:
                plate_well = extract_plate_well(sample_id_label)
                if not plate_well:
                    continue
                sample_id = sample_ids_cache.get(plate_well) or find_or_create_sample(session, cohort, plate_well).id
                sample_ids_cache[plate_well] = sample_id

                if not pd.isnull(row[sample_id_label]):
                    values.append("({}, {}, {}, {})".format(sample_id, cohort_compound.id, dataset.id, row[sample_id_label]))
            if args.verbose:
                print "Inserting {} measurements for metabolite {}.  Row count is {}".format(len(values), cohort_compound.local_compound_id, row_count)
            if len(values):
                sql += ",".join(values)
                session.execute(sql)
                session.commit()
