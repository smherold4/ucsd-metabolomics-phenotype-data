import csv
from models import *
from db import db_connection
import pandas as pd

CSV_CHUNKSIZE = 100000
COLUMNS = {
    'cohort_sample_id_label': 0,
    'plate_well': 1,
    'sample_barcode': 2
}


def run(args):
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(
        args.cohort_name)

    line_count = 0
    for df in pd.read_csv(args.file, chunksize=CSV_CHUNKSIZE):
        cohort.cohort_sample_id_label = df.columns[COLUMNS['cohort_sample_id_label']]
        session.add(cohort)
        session.commit()
        for _, row in df.iterrows():
            line_count += 1
            cohort_sample_id = row[COLUMNS['cohort_sample_id_label']]
            plate_well = row[COLUMNS['plate_well']]
            sample_barcode = row[COLUMNS['sample_barcode']]
            if pd.isnull(cohort_sample_id):
                continue
            subject = session.query(Subject).filter(
                Subject.cohort_id == cohort.id,
                Subject.local_subject_id == cohort_sample_id
            ).first() or Subject(
                cohort,
                cohort_sample_id,
            )
            subject.plate_well = plate_well
            subject.sample_barcode = sample_barcode
            session.add(subject)
            session.commit()
            if args.verbose:
                print 'Saved Sample {} with Sample Barcode {}'.format(cohort_sample_id, sample_barcode)
