import csv
from models import Study, Cohort, CohortCompound, Subject, Sample
from db import db_connection

LOCAL_SUBJECT_ID_COL = 0
FIRST_COL_WITH_MEASUREMENTS = 2
ROW_OF_LOCAL_COMPOUND_ID = 0


def map_local_id_to_cohort_compounds(local_compound_ids, cohort, session):
    all_cohort_compounds = session.query(CohortCompound) \
        .filter(
        CohortCompound.cohort_id == cohort.id,
        CohortCompound.local_compound_id.in_(local_compound_ids)
    ).all()
    assert len(all_cohort_compounds) == len(local_compound_ids), \
        "Some compounds could not be found.  Only found {} compounds for {} local compound IDs" \
        .format(len(all_cohort_compounds), len(local_compound_ids))
    all_cohort_compounds_dict = {
        cc.local_compound_id: cc for cc in all_cohort_compounds}
    import pdb
    pdb.set_trace()
    return [all_cohort_compounds_dict[local_compound_id]
            for local_compound_id in local_compound_ids]


def run(args):
    session = db_connection.session_factory()
    study = session.query(Study).filter(Study.name == args.study_name).first()
    assert study is not None, "Could not find study with name '{}'".format(
        args.study_name)
    cohort = session.query(Cohort).filter(
        Cohort.study_id == study.id,
        Cohort.method == args.method,
        Cohort.units == args.units).first()
    assert cohort is not None, "A cohort with these parameters (study_id, method, units) does not exist"

    cohort_compounds = []
    with open(args.file) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for line_count, row in enumerate(csv_reader):
            row_trimmed = row[FIRST_COL_WITH_MEASUREMENTS:]
            if line_count == 0:
                cohort_compounds = map_local_id_to_cohort_compounds(
                    row_trimmed, cohort, session)
                import pdb
                pdb.set_trace()
            else:
                subject = Subject(cohort, row[LOCAL_SUBJECT_ID_COL])
                session.add(subject)
                session.commit()
                for column, measurement in enumerate(row_trimmed):
                    if not measurement:
                        continue
                    cohort_compound = cohort_compounds[column]
                    sample = Sample(subject, cohort_compound, measurement)
                    session.add(sample)
                    session.commit()
