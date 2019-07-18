import csv
from models import Study, Cohort, CohortCompound, Compound
from db import db_connection

COLUMNS = {
  'local_compound_id': 0,
  'mz': 1,
  'rt': 2,
  'cross_variation': 8,
  'ml_score': 9,
}

def validate_args(args):
  if not args.skip_alignment:
    assert args.alignment_file and args.alignment_cohort_study and args.alignment_cohort_column, "Must have all required arguments --alignment-file, --alignment-cohort-study, --alignment-cohort-column"
    assert args.alignment_cohort_column in ['A', 'B'], "--alignmet-cohort-column must be either 'A' or 'B'"
  assert args.study_id or args.study_name, 'Missing --study-id or --study-name'
  assert args.method in Cohort.METHODS, 'Invalid study method (--method) provided. Must be one of: {}'.format(Cohort.METHODS)
  assert args.units in Cohort.UNITS, 'Invalid units provided. Must be one of: {}'.format(Cohort.UNITS)

def build_lab_id_to_compound_id_mapping(args, alignment_cohort, session):
  result = {}
  cols = { 'A': 0, 'B': 1 }
  alignment_cohort_col = cols[args.alignment_cohort_column]
  new_cohort_col = 1 - alignment_cohort_col
  with open(args.alignment_file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for line_count, row in enumerate(csv_reader):
      if line_count == 0:
        continue
      alignment_cohort_local_cid = row[alignment_cohort_col]
      new_cohort_local_cid = int(row[new_cohort_col])
      alignment_cohort_compound = session.query(CohortCompound) \
        .filter(CohortCompound.cohort_id==alignment_cohort.id, CohortCompound.local_compound_id==alignment_cohort_local_cid) \
        .first()
      result[new_cohort_local_cid] = alignment_cohort_compound.compound_id
    return result

def find_alignment_cohort(args, session):
  alignment_study = session.query(Study).filter(Study.name==args.alignment_cohort_study).first()
  assert alignment_study is not None, "Could not find alignment study with name {}".format(args.alignment_cohort_study)
  alignment_cohort = session \
                       .query(Cohort) \
                       .filter(
                         Cohort.study_id==alignment_study.id,
                         Cohort.method==args.method,
                         Cohort.units==args.units) \
                       .first()
  assert alignment_cohort is not None, "Could not find alignment cohort for study: {}, method: {}, units: {}".format(args.alignment_cohort_study, args.method, args.units)
  return alignment_cohort

def create_compound(csv_row, session):
  mz = csv_row[COLUMNS['mz']]
  rt = csv_row[COLUMNS['rt']]
  compound = Compound(mz, rt)
  session.add(compound)
  session.commit()
  return compound

def existing_compound(csv_row, alignment_mapping, session):
  local_compound_id = csv_row[COLUMNS['local_compound_id']]
  compound_id = alignment_mapping.get(int(local_compound_id))
  if compound_id:
    return session.query(Compound).get(compound_id)

def create_cohort_compound(cohort, compound, csv_row, session):
  local_compound_id = csv_row[COLUMNS['local_compound_id']]
  cross_variation = csv_row[COLUMNS['cross_variation']] or None
  ml_score = csv_row[COLUMNS['ml_score']] or None
  cohort_compound = CohortCompound(cohort, compound, local_compound_id, cross_variation, ml_score)
  session.add(cohort_compound)
  session.commit()

def run(args):
  validate_args(args)
  session = db_connection.session_factory()
  study = None
  if args.study_id:
    study = session.query(Study).get(args.study_id)
    assert study is not None, "Could not find study with id {}".format(args.study_id)
  elif args.study_name:
    study = session.query(Study).filter(Study.name==args.study_name).first()
    assert study is not None, "Could not find study with name '{}'".format(args.study_name)
  
  alignment_cohort = None
  alignment_mapping = {}
  if not args.skip_alignment:
    alignment_cohort = find_alignment_cohort(args, session)
    alignment_mapping = build_lab_id_to_compound_id_mapping(args, alignment_cohort, session)

  cohort = session.query(Cohort).filter(Cohort.study_id==study.id, Cohort.method==args.method, Cohort.units==args.units).first()
  assert cohort is None, "A cohort with these parameters (study_id, method, units) already exists"
  cohort = Cohort(study, args.method, args.units)
  session.add(cohort)
  session.commit()
  
  with open(args.file) as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    for line_count, row in enumerate(csv_reader):
      if line_count == 0:
        continue
      compound = existing_compound(row, alignment_mapping, session) or create_compound(row, session)
      create_cohort_compound(cohort, compound, row, session)
