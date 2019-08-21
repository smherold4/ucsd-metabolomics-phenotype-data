import csv
from models import *
from db import db_connection
import pandas as pd

CSV_CHUNKSIZE = 100000
COLUMNS = {
    'cohort_sample_id_label': 2,
    'plate_well': 1,
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
        cohort.cohort_sample_id_label = df.columns[COLUMNS['cohort_sample_id_label']]
        session.add(cohort)
        session.commit()
        for _, row in df.iterrows():
            line_count += 1
            # maybe the subject will be created after the sample, i don't know
            # for FR and FHS, the local_subject_id is the cohort_sample_id
            local_subject_id = row[COLUMNS['cohort_sample_id_label']]
            cohort_sample_id = row[COLUMNS['cohort_sample_id_label']]
            plate_well = row[COLUMNS['plate_well']]
            if pd.isnull(local_subject_id):
                continue
            subject = find_or_create_subject(session, cohort, local_subject_id)
            if pd.isnull(plate_well):
                continue
            if args.exam_no:
                cohort_sample_id = str(cohort_sample_id) + "-" + args.exam_no
            sample = session.query(Sample).filter(
                Sample.cohort_sample_id == str(cohort_sample_id),
                Sample.cohort_id == cohort.id,
            ).first()
            if not sample:
                if args.verbose:
                    print "Could not find sample with cohort_sample_id {}".format(cohort_sample_id)
                continue
            sample.subject_id = subject.id
            sample.plate_well = plate_well
            if args.exam_no:
                sample.exam_no = args.exam_no
            session.add(sample)
            session.commit()
            if args.verbose:
                print 'Saved cohort_sample_id {} with plate_well {}'.format(sample.cohort_sample_id, sample.plate_well)
