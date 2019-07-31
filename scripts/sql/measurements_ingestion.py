import csv
import pandas as pd
from models import *
from db import db_connection

COHORT_SAMPLE_ID_COL = 0
FIRST_COL_WITH_MEASUREMENTS = 2
ROW_OF_LOCAL_COMPOUND_ID = 0
CSV_CHUNKSIZE = 20


def cohort_compound_ids_by_column(local_compound_ids, cohort, session):
    cohort_compounds = session.query(CohortCompound).filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.local_compound_id.in_(local_compound_ids)).all()
    assert len(cohort_compounds) == len(local_compound_ids), "Some compounds could not be found.  Only found {} compounds for {} local compound IDs".format(
        len(cohort_compounds), len(local_compound_ids))
    id_map = {
        cc.local_compound_id: cc.id for cc in cohort_compounds}
    return [id_map[local_compound_id] for local_compound_id in local_compound_ids]


def build_insert_measurements_sql(measurements, cohort_compound_ids, sample_id, dataset_id):
    insert_values = ["({}, {}, {}, {})".format(sample_id, cohort_compound_ids[column], measurement, dataset_id)
                     for column, measurement in enumerate(measurements) if not pd.isnull(measurement)]
    return "INSERT INTO {} (sample_id, cohort_compound_id, measurement, dataset_id) VALUES ".format(Measurement.__tablename__) + ",".join(insert_values)


def run(args):
    assert args.units in Dataset.UNITS, 'Invalid units provided. Must be one of: {}'.format(Dataset.UNITS)
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)
    dataset = session.query(Dataset).filter(
        Dataset.cohort_id == cohort.id,
        Dataset.units == args.units).first()
    assert dataset is None, "A dataset with these parameters ('{}', '{}') already exists".format(cohort.name, args.units)
    dataset = Dataset(cohort, args.units)
    session.add(dataset)
    session.commit()
    dataset = session.query(Dataset).filter(
        Dataset.cohort_id == cohort.id,
        Dataset.units == args.units).first()
    assert dataset is not None, "A dataset with these parameters ({}, {}) does not exist".format(cohort.name, args.units)

    cohort_compound_ids = []
    line_count = 0
    for df in pd.read_csv(args.file, chunksize=CSV_CHUNKSIZE):
        if line_count == 0:
            local_compound_ids = df.columns[FIRST_COL_WITH_MEASUREMENTS:].tolist()
            cohort_compound_ids = cohort_compound_ids_by_column(local_compound_ids, cohort, session)
        for _, row in df.iterrows():
            line_count += 1
            row_trimmed = row[FIRST_COL_WITH_MEASUREMENTS:].tolist()
            cohort_sample_id = row[COHORT_SAMPLE_ID_COL].strip()
            if pd.isnull(cohort_sample_id):
                continue
            sample = session.query(Sample).join(Sample.subject).filter(
                Subject.cohort_id == cohort.id,
                Sample.cohort_sample_id == cohort_sample_id).first()
            if sample is None:
                if args.verbose:
                    print "Could not find cohort_sample_id {} for cohort {}".format(cohort_sample_id, cohort.name)
                continue
            insert_measurements_sql = build_insert_measurements_sql(row_trimmed, cohort_compound_ids, sample.id, dataset.id)
            if args.verbose:
                print "Inserting measurements for row {}, cohort_sample_id {}".format(line_count, cohort_sample_id)
            session.execute(insert_measurements_sql)
            session.commit()
