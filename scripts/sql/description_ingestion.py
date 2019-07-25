import csv
from models import *
from db import db_connection

COLUMNS = {
    'local_compound_id': 0,
    'mz': 1,
    'rt': 2,
    'cross_variation': 8,
    'ml_score': 9,
}


def build_lab_id_to_compound_id_mapping(args, alignment_cohort, session):
    return {}


def find_cohort_compound(cohort, local_compound_id, session):
    return session.query(CohortCompound).filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.local_compound_id == local_compound_id,
    ).first()


def create_cohort_compound(cohort, compound_row, session):
    local_compound_id = compound_row[COLUMNS['local_compound_id']]
    mz = compound_row[COLUMNS['mz']]
    rt = compound_row[COLUMNS['rt']]
    cross_variation = compound_row[COLUMNS['cross_variation']] or None
    ml_score = compound_row[COLUMNS['ml_score']] or None
    cohort_compound = CohortCompound(
        cohort,
        local_compound_id,
        mz,
        rt,
        cross_variation,
        ml_score)
    session.add(cohort_compound)
    session.commit()


def run(args):
    session = db_connection.session_factory()
    cohort = session.query(Cohort).filter(Cohort.name == args.cohort_name).first()
    assert cohort is not None, "Could not find cohort with name '{}'".format(
        args.cohort_name)

    dataset = session.query(Dataset).filter(
        Dataset.cohort_id == cohort.id,
        Dataset.units == args.units).first()
    assert dataset is None, "A dataset with these parameters ('{}', '{}') already exists".format(cohort.name, args.units)
    dataset = Dataset(cohort, args.units)
    session.add(dataset)
    session.commit()

    with open(args.file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            if line_count == 0:
                continue
            local_compound_id = row[COLUMNS['local_compound_id']]
            find_cohort_compound(cohort, local_compound_id, session) or create_cohort_compound(cohort, row, session)
