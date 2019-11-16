import csv
from models import *
from db import db_connection
import pandas as pd
import re

CSV_CHUNKSIZE = 100000
KEY_COLUMNS = {
    'cohort_sample_id': 0,
    'plate_well': 1,
    'sample_barcode': 4,
}


def find_or_create_subject(session, cohort, local_subject_id):
    subject = session.query(Subject).filter(
        Subject.cohort_id == cohort.id,
        Subject.local_subject_id == str(local_subject_id),
    ).first() or Subject(
        cohort,
        local_subject_id,
    )
    session.add(subject)
    session.commit()
    return subject


def run(args):
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(args.cohort_name)

    line_count = 0
    for df in pd.read_csv(args.file, chunksize=CSV_CHUNKSIZE):
        for _, row in df.iterrows():
            line_count += 1
            cohort_sample_id = local_subject_id = row[KEY_COLUMNS['cohort_sample_id']]
            plate_well = row[KEY_COLUMNS['plate_well']]
            sample_barcode = row[KEY_COLUMNS['sample_barcode']]
            if pd.isnull(plate_well) or pd.isnull(local_subject_id):
                continue
            sample = session.query(Sample).filter(
                Sample.plate_well == str(plate_well),
                Sample.cohort_id == cohort.id,
            ).first()
            if not sample:
                print "Could not find sample with plate_well {}".format(plate_well)
                continue
            subject = find_or_create_subject(session, cohort, local_subject_id)
            sample.subject_id = subject.id
            sample.cohort_sample_id = local_subject_id
            sample.sample_barcode = sample_barcode
            session.add(sample)
            session.commit()
            print 'Saved cohort_sample_id {} with plate_well {}'.format(sample.cohort_sample_id, sample.plate_well)
