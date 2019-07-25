import csv
import pandas as pd
from models import *
from db import db_connection

LOCAL_SUBJECT_ID_COL = 0
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


def find_or_create_subject(cohort, local_subject_id, session):
    subject = session.query(Subject).filter(
        Subject.cohort_id == cohort.id,
        Subject.local_subject_id == local_subject_id).first() or Subject(
        cohort,
        local_subject_id)
    session.add(subject)
    session.commit()
    return subject


def build_insert_measurements_sql(measurements, cohort_compound_ids, subject_id, dataset_id):
    # insert_values = ["({}, {}, {})".format(subject_id,
    # cohort_compound_ids[column]., measurement) for column, measurement in
    # enumerate(measurements) if measurement]
    insert_values = ["({}, {}, {}, {})".format(subject_id, cohort_compound_ids[column], measurement, dataset_id)
                     for column, measurement in enumerate(measurements) if not pd.isnull(measurement)]
    return "INSERT INTO measurement (subject_id, cohort_compound_id, measurement, dataset_id) VALUES " + ",".join(insert_values)


def run(args):
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(
        args.cohort_name)
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
            local_subject_id = row[LOCAL_SUBJECT_ID_COL].strip()
            if pd.isnull(local_subject_id):
                continue
            subject = find_or_create_subject(cohort, local_subject_id, session)
            insert_measurements_sql = build_insert_measurements_sql(row_trimmed, cohort_compound_ids, subject.id, dataset.id)
            if args.verbose:
                print "Inserting measurements for row {}, subjectId {}".format(line_count, local_subject_id)
            session.execute(insert_measurements_sql)
